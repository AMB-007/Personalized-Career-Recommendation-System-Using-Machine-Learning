"""
Assessment Question Selection Engine.
Selects a balanced, grade-appropriate, and difficulty-curated subset of questions
from the master question pool in MySQL for each student assessment session.
Guarantees section quotas, core cognitive ability coverage, and stream filtering.
"""

import json
from typing import List, Dict, Any, Optional
from backend.models.question import Question, QuestionSection


class AssessmentSelectionService:
    """Intelligent adaptive question selection and balancing service."""

    # Target question counts per student grade cohort
    COHORT_TARGETS = {
        'middle_school': {'min_class': 7, 'max_class': 8, 'target_count': 35, 'difficulty_pref': ['Easy', 'Medium']},
        'secondary': {'min_class': 9, 'max_class': 10, 'target_count': 45, 'difficulty_pref': ['Easy', 'Medium', 'Hard']},
        'higher_secondary': {'min_class': 11, 'max_class': 12, 'target_count': 55, 'difficulty_pref': ['Medium', 'Hard', 'Easy']}
    }

    # Minimum questions required per section for a balanced assessment
    SECTION_QUOTAS = {
        # Section ID: (Min Count Middle School, Min Count Secondary, Min Count Higher Sec)
        1: (2, 2, 2),   # Academic Profile
        2: (4, 5, 5),   # Mathematical Ability
        3: (3, 4, 4),   # Logical Reasoning
        4: (3, 4, 4),   # Scientific Thinking
        5: (2, 3, 3),   # Problem Solving
        6: (1, 3, 3),   # Analytical Thinking
        7: (1, 2, 2),   # Communication
        8: (1, 2, 2),   # Creativity
        9: (1, 2, 3),   # Digital Ability
        10: (1, 2, 2),  # Learning Ability
        11: (1, 2, 2),  # Spatial Ability
        12: (1, 2, 2),  # Practical Ability
        13: (6, 8, 10), # Interests
        14: (3, 4, 5),  # Activities
        15: (1, 1, 1),  # Teamwork
        16: (1, 1, 1),  # Leadership
        17: (1, 2, 2),  # Work Preferences
        18: (1, 1, 1),  # Career Awareness
        19: (1, 1, 1)   # Career Preferences
    }

    @classmethod
    def get_cohort_key(cls, class_level: int) -> str:
        """Determines the cohort grouping for a given class level."""
        if class_level in [7, 8]:
            return 'middle_school'
        elif class_level in [9, 10]:
            return 'secondary'
        else:
            return 'higher_secondary'

    @classmethod
    def select_balanced_questions(
        cls,
        class_level: int,
        stream: Optional[str] = None
    ) -> List[Question]:
        """
        Selects a balanced, curated subset of questions from the master question bank.
        1. Queries all eligible active questions for class_level and stream.
        2. Groups questions by section_id and difficulty.
        3. Fulfills guaranteed section quotas and ability coverage.
        4. Reaches exact cohort target count while prioritizing cohort-appropriate difficulty.
        5. Returns the selected questions ordered by section and display order.
        """
        cohort_key = cls.get_cohort_key(class_level)
        cohort_config = cls.COHORT_TARGETS[cohort_key]
        target_count = cohort_config['target_count']
        diff_priority = cohort_config['difficulty_pref']

        # Determine index for quota tuple (0 for middle, 1 for secondary, 2 for higher secondary)
        quota_idx = 0 if cohort_key == 'middle_school' else (1 if cohort_key == 'secondary' else 2)

        # 1. Fetch eligible question pool from MySQL
        query = Question.query.filter(
            Question.is_active == True,
            Question.class_min <= class_level,
            Question.class_max >= class_level
        )

        clean_stream = (stream or 'General').strip()
        if clean_stream.lower() not in ['all', 'general']:
            prefix = clean_stream.split('-')[0].strip()
            query = query.filter(
                (Question.stream_specific == 'All') |
                (Question.stream_specific == 'General') |
                (Question.stream_specific.ilike(f"%{prefix}%"))
            )
        else:
            query = query.filter(
                (Question.stream_specific == 'All') |
                (Question.stream_specific == 'General') |
                (Question.stream_specific.is_(None))
            )

        eligible_pool = query.order_by(Question.section_id.asc(), Question.display_order.asc()).all()

        # 2. Group pool by section_id
        section_buckets: Dict[int, List[Question]] = {}
        for q in eligible_pool:
            section_buckets.setdefault(q.section_id, []).append(q)

        selected_questions_map: Dict[int, Question] = {}

        # 3. Step 1: Satisfy Minimum Section Quotas
        for section_id, q_list in section_buckets.items():
            min_required = cls.SECTION_QUOTAS.get(section_id, (1, 1, 1))[quota_idx]
            
            # Sort within section by difficulty priority match
            sorted_q = sorted(
                q_list,
                key=lambda q: (
                    diff_priority.index(q.difficulty) if q.difficulty in diff_priority else 99,
                    q.display_order
                )
            )

            # Pick up to min_required from this section
            picked = sorted_q[:min_required]
            for q in picked:
                selected_questions_map[q.id] = q

        # 4. Step 2: Fill remaining slots up to target_count using preferred difficulty distribution
        remaining_pool = [q for q in eligible_pool if q.id not in selected_questions_map]
        
        # Sort remaining pool prioritizing cohort difficulty and section balance
        sorted_remaining = sorted(
            remaining_pool,
            key=lambda q: (
                diff_priority.index(q.difficulty) if q.difficulty in diff_priority else 99,
                q.section_id,
                q.display_order
            )
        )

        slots_needed = target_count - len(selected_questions_map)
        if slots_needed > 0:
            for q in sorted_remaining[:slots_needed]:
                selected_questions_map[q.id] = q

        # 5. Return final selected questions in natural section and display order
        final_list = sorted(
            selected_questions_map.values(),
            key=lambda q: (q.section_id, q.display_order, q.id)
        )
        return final_list
