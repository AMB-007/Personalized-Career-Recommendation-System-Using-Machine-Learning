"""
Assessment Question Selection & Balancing Test Suite.
Verifies cohort question counts, section quotas, difficulty distributions,
stream filtering, and session persistence across page refreshes.
"""

import os
import sys
import unittest
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app import create_app
from backend.extensions import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.question import Question, QuestionSection, QuestionOption
from backend.models.assessment import AssessmentSession
from backend.services.assessment_selection_service import AssessmentSelectionService
from backend.services.assessment_service import AssessmentService
from database.build_questions_dataset import MASTER_QUESTIONS


class TestAssessmentSelection(unittest.TestCase):
    """Unit tests for AssessmentSelectionService."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        # Seed sections
        sections_data = [
            (1, 'Academic Profile'), (2, 'Mathematical Ability'), (3, 'Logical Reasoning'),
            (4, 'Scientific Thinking'), (5, 'Problem Solving'), (6, 'Analytical Thinking'),
            (7, 'Communication'), (8, 'Creativity'), (9, 'Digital Ability'),
            (10, 'Learning Ability'), (11, 'Spatial Ability'), (12, 'Practical Ability'),
            (13, 'Interests'), (14, 'Activities'), (15, 'Teamwork'),
            (16, 'Leadership'), (17, 'Work Preferences'), (18, 'Career Awareness'),
            (19, 'Career Preferences')
        ]
        for s_id, s_name in sections_data:
            sec = QuestionSection(id=s_id, name=s_name, display_order=s_id, is_active=True)
            db.session.add(sec)
        db.session.commit()

        # Seed master questions
        for q in MASTER_QUESTIONS:
            q_obj = Question(
                question_code=q['question_code'],
                question_text=q['question_text'],
                section_id=q['section_id'],
                question_type=q['question_type'],
                class_min=q['class_min'],
                class_max=q['class_max'],
                difficulty=q['difficulty'],
                skill_category=q['skill_category'],
                stream_specific=q['stream_specific'],
                is_required=True,
                display_order=q['display_order'],
                is_active=True
            )
            db.session.add(q_obj)
            db.session.flush()

            for opt in q.get('options', []):
                opt_obj = QuestionOption(
                    question_id=q_obj.id,
                    option_text=opt['option_text'],
                    option_value=opt['option_value'],
                    score=float(opt.get('score', 0.0)),
                    is_correct=bool(opt.get('is_correct', False)),
                    display_order=opt.get('display_order', 1)
                )
                db.session.add(opt_obj)

        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_cohort_target_counts(self):
        """Verify selected question count falls into target bounds for all classes."""
        # Class 7-8: 30-40 questions
        for c in [7, 8]:
            selected = AssessmentSelectionService.select_balanced_questions(c)
            self.assertGreaterEqual(len(selected), 30, f"Class {c} question count < 30: {len(selected)}")
            self.assertLessEqual(len(selected), 40, f"Class {c} question count > 40: {len(selected)}")

        # Class 9-10: 40-50 questions
        for c in [9, 10]:
            selected = AssessmentSelectionService.select_balanced_questions(c)
            self.assertGreaterEqual(len(selected), 40, f"Class {c} question count < 40: {len(selected)}")
            self.assertLessEqual(len(selected), 50, f"Class {c} question count > 50: {len(selected)}")

        # Class 11-12: 50-60 questions
        for c in [11, 12]:
            for stream in ['Science-PCM', 'Commerce', 'Humanities']:
                selected = AssessmentSelectionService.select_balanced_questions(c, stream=stream)
                self.assertGreaterEqual(len(selected), 50, f"Class {c} ({stream}) question count < 50: {len(selected)}")
                self.assertLessEqual(len(selected), 60, f"Class {c} ({stream}) question count > 60: {len(selected)}")

    def test_section_coverage_across_cohorts(self):
        """Verify selected questions include all major sections and ability dimensions."""
        for c in [7, 9, 11]:
            stream = 'Science-PCM' if c == 11 else 'General'
            selected = AssessmentSelectionService.select_balanced_questions(c, stream=stream)
            section_ids = set(q.section_id for q in selected)

            # Ensure presence of cognitive & interest sections
            for s_id in range(1, 20):
                self.assertIn(s_id, section_ids, f"Class {c} missing Section ID {s_id}")

    def test_difficulty_balancing(self):
        """Verify difficulty distribution matches pedagogical cohort guidelines."""
        # Class 7: mostly Easy + Medium across all questions
        sel_7 = AssessmentSelectionService.select_balanced_questions(7)
        diff_7 = Counter(q.difficulty for q in sel_7)
        self.assertGreater(diff_7.get('Easy', 0) + diff_7.get('Medium', 0), diff_7.get('Hard', 0))

        # Class 11: Cognitive questions (Sections 1-12) are predominantly Medium + Hard
        sel_11 = AssessmentSelectionService.select_balanced_questions(11, stream='Science-PCM')
        cognitive_q11 = [q for q in sel_11 if q.section_id <= 12]
        diff_cog11 = Counter(q.difficulty for q in cognitive_q11)
        self.assertGreater(diff_cog11.get('Medium', 0) + diff_cog11.get('Hard', 0), diff_cog11.get('Easy', 0))

    def test_session_question_persistence_on_refresh(self):
        """Verify session.selected_question_ids preserves exact questions across multiple retrievals."""
        user = User(username='sel_test_user', email='sel_test@test.com', role='student')
        user.set_password('Pass1234!')
        db.session.add(user)
        db.session.commit()

        student = Student(user_id=user.id, student_code='STU-SEL-01', first_name='Sel', last_name='Test', class_level=10, stream='General')
        db.session.add(student)
        db.session.commit()

        # Start session
        session = AssessmentService.start_new_session(student.id)
        self.assertIsNotNone(session.selected_question_ids)

        # First retrieval
        q_first = AssessmentService.get_questions_for_session(session)
        q_first_ids = [q.id for q in q_first]

        # Simulate page refresh / subsequent retrieval
        q_second = AssessmentService.get_questions_for_session(session)
        q_second_ids = [q.id for q in q_second]

        self.assertEqual(q_first_ids, q_second_ids, "Questions changed on session re-fetch / refresh!")


if __name__ == '__main__':
    unittest.main()
