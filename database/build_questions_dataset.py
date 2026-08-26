"""
Comprehensive Student Question Bank Builder & Exporter.
Defines, validates, and seeds high-quality adaptive assessment questions for Class 7-12
across all 19 standardized assessment sections with multi-dimensional ML feature mappings.
Generates database/questions_seed.json and database/questions_seed.sql.
"""

import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


# Helper function to generate standardized 5-point rating options
def make_rating_options(low_label="Not Interested", high_label="Very Interested"):
    return [
        {"option_text": f"1 - {low_label}", "option_value": "1", "score": 20.0, "is_correct": False, "display_order": 1},
        {"option_text": "2 - Slight", "option_value": "2", "score": 40.0, "is_correct": False, "display_order": 2},
        {"option_text": "3 - Moderate / Neutral", "option_value": "3", "score": 60.0, "is_correct": False, "display_order": 3},
        {"option_text": "4 - High", "option_value": "4", "score": 80.0, "is_correct": False, "display_order": 4},
        {"option_text": f"5 - {high_label}", "option_value": "5", "score": 100.0, "is_correct": False, "display_order": 5}
    ]


# Helper function to generate activity frequency options
def make_frequency_options():
    return [
        {"option_text": "1 - Never", "option_value": "1", "score": 20.0, "is_correct": False, "display_order": 1},
        {"option_text": "2 - Rarely", "option_value": "2", "score": 40.0, "is_correct": False, "display_order": 2},
        {"option_text": "3 - Sometimes", "option_value": "3", "score": 60.0, "is_correct": False, "display_order": 3},
        {"option_text": "4 - Often", "option_value": "4", "score": 80.0, "is_correct": False, "display_order": 4},
        {"option_text": "5 - Very Often", "option_value": "5", "score": 100.0, "is_correct": False, "display_order": 5}
    ]


# ------------------------------------------------------------
# Master Question Definitions across All 19 Sections
# ------------------------------------------------------------

MASTER_QUESTIONS = [
    # ========================================================
    # SECTION 1: ACADEMIC (Section ID: 1)
    # ========================================================
    {
        "question_code": "ACAD_01_FAV_78",
        "question_text": "Which school subject do you naturally look forward to the most during the week?",
        "section_id": 1, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Identifies foundational subject inclinations in middle school.",
        "options": [
            {"option_text": "Mathematics and numbers", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Science experiments and nature", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Computers and technology", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Social studies, languages, or art", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ACAD_02_STUDY_78",
        "question_text": "How do you prefer to learn and understand new concepts in class?",
        "section_id": 1, "question_type": "RATING", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Assesses preference for active hands-on exploration versus passive reading.",
        "options": make_rating_options("Passive Memorization", "Hands-on Practical Exploration")
    },
    {
        "question_code": "ACAD_03_STREAM_INT_910",
        "question_text": "When planning for Class 11 and 12, which academic stream currently aligns closest with your goals?",
        "section_id": 1, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Measures secondary student stream inclination ahead of high school transition.",
        "options": [
            {"option_text": "Science (Physics, Chemistry, Mathematics / Biology)", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Commerce (Accountancy, Business Studies, Economics)", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Humanities / Arts (History, Political Science, Psychology)", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Applied Vocational / Computer Applications / Design", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ACAD_04_CONF_910",
        "question_text": "How confident do you feel when preparing for complex board-level conceptual exam questions?",
        "section_id": 1, "question_type": "RATING", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "Evaluates self-efficacy and academic resilience under rigorous evaluation.",
        "options": make_rating_options("Highly Anxious", "Fully Prepared & Confident")
    },
    {
        "question_code": "ACAD_05_PREP_1112",
        "question_text": "What is your primary preparation focus alongside your Class 11-12 curriculum?",
        "section_id": 1, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 5,
        "explanation": "Captures post-secondary trajectory and competitive entrance examination focus.",
        "options": [
            {"option_text": "National competitive entrance exams (JEE, NEET, NDA, CLAT, CUET, CA Foundation)", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Board examination excellence and university merit admission", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Building a portfolio / practical projects for design, coding, or entrepreneurship", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Exploring international studies and standardized global tests", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ACAD_SCI_01_1112",
        "question_text": "In your science coursework, which area engages your deepest problem-solving interest?",
        "section_id": 1, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "scientific_reasoning", "stream_specific": "Science", "is_required": True, "display_order": 6,
        "explanation": "Differentiates mathematical-physical sciences (PCM) from biological-clinical sciences (PCB).",
        "options": [
            {"option_text": "Mathematical physics, calculus mechanics, and computing algorithms", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Cellular biology, genetic mechanisms, and physiological biochemistry", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Organic synthesis, molecular structures, and industrial chemical processes", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Experimental lab diagnostics and empirical scientific data analysis", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ACAD_COM_01_1112",
        "question_text": "Which dimension of commerce and enterprise excites your analytical curiosity the most?",
        "section_id": 1, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "analytical_ability", "stream_specific": "Commerce", "is_required": True, "display_order": 7,
        "explanation": "Differentiates financial accounting, economic modeling, and corporate management paths.",
        "options": [
            {"option_text": "Financial statements, taxation laws, auditing, and ledger balance", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Macroeconomic policies, market supply-demand curves, and monetary policy", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Stock market investing, venture capital, and corporate valuation", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Business strategy, marketing psychology, and supply chain operations", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ACAD_HUM_01_1112",
        "question_text": "In humanities and social studies, which core area do you find most intellectually compelling?",
        "section_id": 1, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "analytical_ability", "stream_specific": "Humanities", "is_required": True, "display_order": 8,
        "explanation": "Differentiates legal-policy, psychological, and historical-literary pathways.",
        "options": [
            {"option_text": "Constitutional law, governance systems, and international diplomacy", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Human cognitive behavior, developmental psychology, and social counseling", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Historical revolutions, archaeological heritage, and geopolitical dynamics", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Literature, journalism, investigative media, and sociological field research", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 2: MATHEMATICAL ABILITY (Section ID: 2)
    # ========================================================
    {
        "question_code": "MATH_01_SEQ_78",
        "question_text": "What is the next number in the square-based sequence: 4, 9, 16, 25, 36, ...?",
        "section_id": 2, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "The terms represent consecutive squares: 2^2=4, 3^2=9, 4^2=16, 5^2=25, 6^2=36, so next is 7^2 = 49.",
        "options": [
            {"option_text": "45", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "47", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "49", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "52", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_02_PERC_78",
        "question_text": "A book priced at ₹400 is offered at a 25% discount. What is its final selling price?",
        "section_id": 2, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Discount = 25% of 400 = ₹100. Final Price = 400 - 100 = ₹300.",
        "options": [
            {"option_text": "₹280", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "₹300", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "₹320", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "₹350", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_03_RATIO_78",
        "question_text": "If a recipe requires flour and sugar in the ratio 3:2, how much sugar is needed for 450 grams of flour?",
        "section_id": 2, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Medium",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Ratio = 3/2 -> 450 / Sugar = 3/2 -> Sugar = (450 * 2) / 3 = 300 grams.",
        "options": [
            {"option_text": "225 grams", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "280 grams", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "300 grams", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "350 grams", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_04_ALG_78",
        "question_text": "If 3x + 15 = 45, what is the value of x?",
        "section_id": 2, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "3x = 45 - 15 = 30 -> x = 30 / 3 = 10.",
        "options": [
            {"option_text": "8", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "10", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "12", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "15", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_05_GEOM_78",
        "question_text": "A rectangular playground has a length of 25 meters and a perimeter of 80 meters. What is its width?",
        "section_id": 2, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Medium",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 5,
        "explanation": "Perimeter = 2*(L + W) = 80 -> L + W = 40 -> W = 40 - 25 = 15 meters.",
        "options": [
            {"option_text": "12 meters", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "15 meters", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "18 meters", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "20 meters", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_06_QUAD_910",
        "question_text": "What are the roots of the quadratic equation x² - 7x + 12 = 0?",
        "section_id": 2, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 6,
        "explanation": "(x - 3)(x - 4) = 0 -> x = 3, 4.",
        "options": [
            {"option_text": "x = 2, 6", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "x = 3, 4", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "x = -3, -4", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "x = 1, 12", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_07_PROB_910",
        "question_text": "Two fair 6-sided dice are rolled simultaneously. What is the probability that the sum of the numbers is 8?",
        "section_id": 2, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Hard",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 7,
        "explanation": "Combinations summing to 8: (2,6), (3,5), (4,4), (5,3), (6,2) -> 5 outcomes out of 36 -> 5/36.",
        "options": [
            {"option_text": "4/36 (1/9)", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "5/36", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "6/36 (1/6)", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "7/36", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_08_COMM_910",
        "question_text": "An investment of ₹10,000 earns compound interest at 10% per annum compounded annually. What is the total amount after 2 years?",
        "section_id": 2, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 8,
        "explanation": "A = P(1 + r/100)^t = 10,000 * (1.1)^2 = 10,000 * 1.21 = ₹12,100.",
        "options": [
            {"option_text": "₹11,500", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "₹12,000", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "₹12,100", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "₹12,500", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_09_STAT_910",
        "question_text": "The marks of 7 students in a test are: 14, 18, 12, 20, 16, 15, 17. What is the median mark?",
        "section_id": 2, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Easy",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 9,
        "explanation": "Arranged in ascending order: 12, 14, 15, 16, 17, 18, 20. The middle (4th) value is 16.",
        "options": [
            {"option_text": "15", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "16", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "16.5", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "17", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_10_TRIG_910",
        "question_text": "A 10-meter ladder leans against a vertical wall making an angle of 60° with the ground. How high up the wall does the ladder reach? (sin 60° = √3/2 ≈ 0.866)",
        "section_id": 2, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 10,
        "explanation": "Height = Hypotenuse * sin(60°) = 10 * 0.866 = 8.66 meters.",
        "options": [
            {"option_text": "5.00 meters", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "7.07 meters", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "8.66 meters", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "10.00 meters", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_11_PERM_1112",
        "question_text": "In how many ways can a committee of 3 students be chosen from a group of 8 candidates?",
        "section_id": 2, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Medium",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 11,
        "explanation": "8C3 = (8 * 7 * 6) / (3 * 2 * 1) = 56 ways.",
        "options": [
            {"option_text": "24", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "48", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "56", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "336", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_12_LOG_1112",
        "question_text": "If log₁₀(x) + log₁₀(x - 3) = 1, what is the valid real value of x?",
        "section_id": 2, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 12,
        "explanation": "log₁₀(x(x - 3)) = 1 -> x² - 3x = 10 -> x² - 3x - 10 = 0 -> (x - 5)(x + 2) = 0. Since log requires positive arguments, x = 5.",
        "options": [
            {"option_text": "x = 2", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "x = 4", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "x = 5", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "x = 10", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_13_MATR_1112",
        "question_text": "What is the determinant of the 2x2 matrix [[4, 3], [2, 5]]?",
        "section_id": 2, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Medium",
        "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 13,
        "explanation": "Determinant = (ad - bc) = (4 * 5) - (3 * 2) = 20 - 6 = 14.",
        "options": [
            {"option_text": "10", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "14", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "26", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "20", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_SCI_02_1112",
        "question_text": "What is the derivative of f(x) = 3x³ - 5x² + 7x - 4 with respect to x?",
        "section_id": 2, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Medium",
        "skill_category": "mathematical_ability", "stream_specific": "Science", "is_required": True, "display_order": 14,
        "explanation": "d/dx(3x^3 - 5x^2 + 7x - 4) = 9x^2 - 10x + 7.",
        "options": [
            {"option_text": "9x² - 10x + 7", "option_value": "A", "score": 1.0, "is_correct": True, "display_order": 1},
            {"option_text": "6x² - 5x + 7", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "9x³ - 10x² + 7", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "3x² - 10x + 4", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "MATH_COM_02_1112",
        "question_text": "A manufacturing unit has fixed costs of ₹50,000, variable cost per unit of ₹30, and selling price per unit of ₹50. What is the break-even quantity?",
        "section_id": 2, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "mathematical_ability", "stream_specific": "Commerce", "is_required": True, "display_order": 15,
        "explanation": "Break-even = Fixed Cost / (Selling Price - Variable Cost) = 50,000 / (50 - 30) = 50,000 / 20 = 2,500 units.",
        "options": [
            {"option_text": "1,800 units", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "2,200 units", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "2,500 units", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "3,000 units", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 3: LOGICAL REASONING (Section ID: 3)
    # ========================================================
    {
        "question_code": "LOGIC_01_SER_78",
        "question_text": "Complete the letter series: AZ, BY, CX, DW, ...?",
        "section_id": 3, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "First letters increase forward (A, B, C, D, E), second letters move backward (Z, Y, X, W, V) -> EV.",
        "options": [
            {"option_text": "EU", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "EV", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "FU", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "FV", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LOGIC_02_ANLG_78",
        "question_text": "Thermometer is to Temperature as Barometer is to:",
        "section_id": 3, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "A thermometer measures temperature; a barometer measures atmospheric pressure.",
        "options": [
            {"option_text": "Humidity", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Atmospheric Pressure", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Wind Velocity", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Rainfall Volume", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LOGIC_03_DIR_78",
        "question_text": "Anil walks 10 meters North, turns right and walks 6 meters, then turns right again and walks 10 meters. In which direction is he from his starting point?",
        "section_id": 3, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Medium",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "10m North, 6m East, 10m South puts him exactly 6 meters East of his start point.",
        "options": [
            {"option_text": "North", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "East", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "South", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "West", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LOGIC_04_CLASS_78",
        "question_text": "Which word does NOT belong with the others in the group?",
        "section_id": 3, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "Guitar, Violin, and Cello are stringed instruments played with fingers/bows; Flute is a wind woodwind instrument.",
        "options": [
            {"option_text": "Guitar", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Violin", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "Flute", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "Cello", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LOGIC_05_SYLL_910",
        "question_text": "Statements: (1) All scientists are curious. (2) Some curious people are inventors. Conclusion: (I) All inventors are scientists. (II) Some scientists might be inventors. Which is logically valid?",
        "section_id": 3, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 5,
        "explanation": "Only conclusion II is a possible logical deduction; I is an invalid overgeneralization.",
        "options": [
            {"option_text": "Only Conclusion I follows", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Only Conclusion II follows", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Both I and II follow", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Neither follows", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LOGIC_06_SEAT_910",
        "question_text": "Five students P, Q, R, S, T sit in a row. S is to the immediate right of P. Q is to the immediate left of P. T is to the right of S. Who is sitting in the middle?",
        "section_id": 3, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 6,
        "explanation": "Order from left to right: Q, P, S, T (with R at the edge). P is flanked by Q and S, placing P in the central position.",
        "options": [
            {"option_text": "Q", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "P", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "S", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "T", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LOGIC_07_CODE_910",
        "question_text": "In a certain code, 'LOGIC' is coded as 'MQHJD' (each letter shifted +1 forward). How is 'BRAIN' coded in that same system?",
        "section_id": 3, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Easy",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 7,
        "explanation": "B->C, R->S, A->B, I->J, N->O -> 'CSBJO'.",
        "options": [
            {"option_text": "CSBJO", "option_value": "A", "score": 1.0, "is_correct": True, "display_order": 1},
            {"option_text": "CRBJO", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "DSCKP", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "BQZHM", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LOGIC_08_COND_1112",
        "question_text": "Consider the rule: 'If a student passes the entrance test (P), they receive a merit scholarship (Q).' Which of the following is logically equivalent to this rule (the contrapositive)?",
        "section_id": 3, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 8,
        "explanation": "The contrapositive of 'If P then Q' is 'If not Q, then not P' (If a student did not receive a merit scholarship, they did not pass the entrance test).",
        "options": [
            {"option_text": "If a student receives a scholarship, they passed the entrance test", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "If a student does not receive a scholarship, they did not pass the entrance test", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "If a student fails the test, they do not get a scholarship", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "A student receives a scholarship only if they fail the test", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LOGIC_09_ASSUMP_1112",
        "question_text": "Statement: 'The school introduced coding classes in Class 6 to prepare students for high-tech future careers.' What assumption is implicitly made?",
        "section_id": 3, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "logical_reasoning", "stream_specific": "All", "is_required": True, "display_order": 9,
        "explanation": "The initiative assumes that early computational foundational training positively equips students for future technological employment requirements.",
        "options": [
            {"option_text": "Every single student in Class 6 will become a professional software engineer", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Early exposure to computational thinking contributes to readiness for technology-driven career landscapes", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "No other subject will be taught in Class 6", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Traditional non-tech careers will vanish completely within two years", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 4: SCIENTIFIC THINKING (Section ID: 4)
    # ========================================================
    {
        "question_code": "SCI_01_EXP_78",
        "question_text": "A student wants to test whether sunlight affects seed germination. Which factor should be changed while keeping all other conditions identical?",
        "section_id": 4, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "scientific_reasoning", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "In a controlled experiment, only the independent variable being tested (light exposure) should vary.",
        "options": [
            {"option_text": "Amount of water given to each pot", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Type of soil used in each pot", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "Exposure to sunlight (dark vs bright)", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "Number of seeds placed in each pot", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SCI_02_DENS_78",
        "question_text": "An iron nail sinks in water, but a huge ship made of iron and steel floats. What scientific principle explains this?",
        "section_id": 4, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Medium",
        "skill_category": "scientific_reasoning", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "The hollow shape of the ship gives it a large volume and air pockets, making its overall average density less than water.",
        "options": [
            {"option_text": "The ship is coated with water-repellent paint", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "The hollow design reduces the ship's average density below that of water", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Ocean water has zero buoyancy force", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Iron changes its chemical properties when heated", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SCI_03_HEAT_78",
        "question_text": "Why are small gaps left between consecutive metal rails on a railway track?",
        "section_id": 4, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "scientific_reasoning", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Metals expand thermally during hot summer temperatures; expansion gaps prevent tracks from buckling.",
        "options": [
            {"option_text": "To save iron and construction costs", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "To allow thermal expansion during hot summer days without track buckling", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "To let rainwater drain into the ground", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "To make the train produce a rhythmic sound", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SCI_04_HYP_910",
        "question_text": "An enzyme reaction speeds up as temperature rises from 20°C to 40°C, but drops sharply above 45°C. What is the most plausible biological hypothesis?",
        "section_id": 4, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "scientific_reasoning", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "Enzymes are protein catalysts; at excessive temperatures (>45°C), their 3D tertiary structure denatures and loses function.",
        "options": [
            {"option_text": "The substrate concentration drops to zero at 45°C", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "High temperature denatures the enzyme's protein active site", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Water molecules evaporate completely at 45°C", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Enzymes turn into lipids at elevated temperatures", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SCI_05_CIRCUIT_910",
        "question_text": "In a series circuit with 3 identical light bulbs, what happens if one bulb burns out (breaks the circuit)?",
        "section_id": 4, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "scientific_reasoning", "stream_specific": "All", "is_required": True, "display_order": 5,
        "explanation": "In a series circuit, there is only one current path; an open break stops current flow to all components.",
        "options": [
            {"option_text": "The other two bulbs shine twice as brightly", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "The other two bulbs go out completely", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "The remaining bulbs flicker intermittently", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "The voltage across the battery increases", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SCI_06_GEN_910",
        "question_text": "In a cross between two heterozygous tall pea plants (Tt x Tt), what percentage of offspring are expected to be short (tt)?",
        "section_id": 4, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "scientific_reasoning", "stream_specific": "All", "is_required": True, "display_order": 6,
        "explanation": "Punnett square for Tt x Tt produces 1 TT (tall), 2 Tt (tall), 1 tt (short) -> 1/4 = 25% short plants.",
        "options": [
            {"option_text": "0%", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "25%", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "50%", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "75%", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SCI_07_EVID_1112",
        "question_text": "A clinical study reports that Drug X reduces fever 20% faster than a placebo, but the sample size was only 6 patients. How should a scientific researcher evaluate this finding?",
        "section_id": 4, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "scientific_reasoning", "stream_specific": "All", "is_required": True, "display_order": 7,
        "explanation": "Small sample sizes have high variance and lack statistical power; results require double-blind randomized trials with large cohorts.",
        "options": [
            {"option_text": "Accept the result immediately as definitive proof", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Reject validity until verified by large-scale randomized controlled trials", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Conclude that fever is completely cured by Drug X", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Publish immediately without peer review", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SCI_08_THERM_1112",
        "question_text": "According to the Second Law of Thermodynamics, in an isolated system during any spontaneous natural process, what happens to the total entropy?",
        "section_id": 4, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "scientific_reasoning", "stream_specific": "Science", "is_required": True, "display_order": 8,
        "explanation": "The Second Law dictates that the total entropy (disorder) of an isolated system always increases over time (ΔS_total > 0).",
        "options": [
            {"option_text": "Entropy always decreases to absolute zero", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Entropy always increases or remains constant in a reversible process", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Entropy transforms directly into gravitational potential energy", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Entropy fluctuates purely at random without direction", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 5: PROBLEM SOLVING (Section ID: 5)
    # ========================================================
    {
        "question_code": "PS_01_QUEUE_78",
        "question_text": "Scenario: During school lunch break, long lines form at the single food counter, causing delays. What is the most effective immediate solution?",
        "section_id": 5, "question_type": "SCENARIO", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "problem_solving", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Separating payment/ordering from collection parallelizes throughput and eliminates bottlenecks.",
        "options": [
            {"option_text": "Tell students to run faster to the canteen", "option_value": "A", "score": 0.2, "is_correct": False, "display_order": 1},
            {"option_text": "Create two separate lines: one for pre-packed tokens and one for food pickup", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Cancel the lunch break", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Serve food only to older students first", "option_value": "D", "score": 0.2, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PS_02_DIAG_78",
        "question_text": "Your computer monitor displays a black screen when turned on, but the CPU power light is green. What is the logical first troubleshooting step?",
        "section_id": 5, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "problem_solving", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Check physical display cable connection and monitor power supply before software or internal hardware diagnosis.",
        "options": [
            {"option_text": "Reinstall the entire operating system", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Check if monitor power and HDMI/video display cable are firmly plugged in", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Replace the computer motherboard immediately", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Delete all browser cache files", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PS_03_TRADE_910",
        "question_text": "Scenario: Your science exhibition team has only 2 days left before submission. The main robot chassis is complete, but the automated audio greeting is buggy. How should you prioritize?",
        "section_id": 5, "question_type": "SCENARIO", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "problem_solving", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Focus on core functional requirements and system stability rather than non-essential cosmetic features under deadline pressure.",
        "options": [
            {"option_text": "Dismantle the entire robot to start over", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Disable the optional audio feature and rigorously test the primary robotic mobility functions", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Spend all remaining time fixing audio while leaving mobility untested", "option_value": "C", "score": 0.3, "is_correct": False, "display_order": 3},
            {"option_text": "Withdraw from the exhibition", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PS_04_ROOT_910",
        "question_text": "A school library reports that book lending dropped 40% in 6 months. What analytical root-cause investigation step should be taken first?",
        "section_id": 5, "question_type": "SCENARIO", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "problem_solving", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "Gather empirical survey data from students regarding catalogue relevance, digital access, and library timings before proposing interventions.",
        "options": [
            {"option_text": "Buy 1,000 random novels without asking anyone", "option_value": "A", "score": 0.1, "is_correct": False, "display_order": 1},
            {"option_text": "Survey students on catalog relevance, digital access, and opening hours to identify friction points", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Impose mandatory library attendance fines on all classes", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Close the library permanently", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PS_05_OPTIM_1112",
        "question_text": "Scenario: A hospital has 3 ambulances and must respond to 5 emergency calls simultaneously in different zones. What strategy optimizes survival outcomes?",
        "section_id": 5, "question_type": "SCENARIO", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "problem_solving", "stream_specific": "All", "is_required": True, "display_order": 5,
        "explanation": "Triage severity scoring coupled with GPS route optimization ensures highest-criticality cases receive immediate response while coordinating secondary dispatch.",
        "options": [
            {"option_text": "Dispatch strictly on a first-come, first-served basis regardless of injury severity", "option_value": "A", "score": 0.2, "is_correct": False, "display_order": 1},
            {"option_text": "Triage by medical severity score and dispatch closest units to critical emergencies while routing non-critical to backup partners", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Wait until all 5 patients are ready before dispatching", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Send all 3 ambulances to the closest hospital", "option_value": "D", "score": 0.1, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PS_06_SYSTEMS_1112",
        "question_text": "When a retail company discounts a product by 50%, store sales surge 200%, but supplier warehouses run out of stock for 3 weeks. What systems-thinking failure occurred?",
        "section_id": 5, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "problem_solving", "stream_specific": "All", "is_required": True, "display_order": 6,
        "explanation": "Failing to integrate upstream supply chain lead-time feedback loops with front-end marketing promotion demand creates stockouts.",
        "options": [
            {"option_text": "The customers bought too many products", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Failure to coordinate demand spikes with upstream supply chain inventory lead times", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "The warehouse workers took too many holidays", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Discounts should be banned by law", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 6: ANALYTICAL THINKING (Section ID: 6)
    # ========================================================
    {
        "question_code": "ANAL_01_CHART_910",
        "question_text": "A line graph shows renewable energy usage rising from 10% in 2015 to 25% in 2020 and 40% in 2025. What is the average annual percentage-point growth rate over the 10-year period?",
        "section_id": 6, "question_type": "MCQ", "class_min": 7, "class_max": 10, "difficulty": "Medium",
        "skill_category": "analytical_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Total growth = 40% - 10% = 30 percentage points over 10 years -> 30 / 10 = 3 percentage points per year.",
        "options": [
            {"option_text": "2.0 percentage points / year", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "3.0 percentage points / year", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "4.5 percentage points / year", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "5.0 percentage points / year", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ANAL_02_CORR_910",
        "question_text": "Ice cream sales and drowning incidents both peak during July. What is the most accurate analytical interpretation?",
        "section_id": 6, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "analytical_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Correlation does not imply causation; both variables are driven by a confounding seasonal factor (hot summer weather and increased swimming).",
        "options": [
            {"option_text": "Eating ice cream causes people to drown", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Both variables correlate with a third confounding factor: hot summer weather", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Drowning incidents cause increased demand for cold ice cream", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "The data is completely fabricated", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ANAL_03_TABLE_910",
        "question_text": "In a survey of 200 students: 120 play sports, 80 play video games, and 40 participate in both. How many students participate in NEITHER activity?",
        "section_id": 6, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "analytical_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Total participating in at least one = 120 + 80 - 40 = 160. Neither = 200 - 160 = 40 students.",
        "options": [
            {"option_text": "20", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "30", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "40", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "50", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ANAL_04_SCAT_1112",
        "question_text": "In a dataset of 500 company employees, years of experience has a correlation of r = +0.82 with salary, but an employee with 20 years experience earns less than entry level. What is this data point called?",
        "section_id": 6, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Medium",
        "skill_category": "analytical_ability", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "An individual data point that deviates markedly from the general trend of the sample is an outlier/anomaly.",
        "options": [
            {"option_text": "Standard Normal Distribution", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Statistical Outlier / Anomaly", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Dependent Variable", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Regression Slope Coefficient", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "ANAL_05_POLICY_1112",
        "question_text": "A city introduces a 10% tax on sugary drinks. Consumption drops 15%, but total calorie intake remains unchanged because consumers buy sweetened baked snacks instead. What analytical concept explains this?",
        "section_id": 6, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "analytical_ability", "stream_specific": "All", "is_required": True, "display_order": 5,
        "explanation": "Cross-price elasticity and the substitution effect describe consumers shifting demand to alternative close substitutes when one good is taxed.",
        "options": [
            {"option_text": "The law of diminishing marginal utility", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Cross-price elasticity and the Substitution Effect", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Monopolistic price gouging", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Random sampling error", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 7: COMMUNICATION (Section ID: 7)
    # ========================================================
    {
        "question_code": "COMM_01_AUD_78",
        "question_text": "Scenario: You are explaining how an electric circuit works to a 6-year-old child. What approach is most effective?",
        "section_id": 7, "question_type": "SCENARIO", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "communication", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Effective communicators tailor technical metaphors to their listener's cognitive frame of reference.",
        "options": [
            {"option_text": "Recite the formal equations for Maxwell's electromagnetic fields", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Use an analogy like water flowing through pipes and turning a waterwheel", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Show a complex 20-page schematic diagram without speaking", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Tell them to wait 10 years until high school", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "COMM_02_DEBATE_910",
        "question_text": "During a structured debate, your opponent raises a factual point that challenges your argument. What is the strongest communication response?",
        "section_id": 7, "question_type": "SCENARIO", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "communication", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Acknowledge valid points constructively and re-anchor your position with nuanced evidence.",
        "options": [
            {"option_text": "Interrupt loudly to prevent the audience from hearing them", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Acknowledge their valid point and reframe your argument with deeper contextual evidence", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Attack their personal background rather than the topic", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Walk off the stage", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "COMM_03_EXEC_1112",
        "question_text": "Scenario: You have 3 minutes to pitch a project proposal to school trustees. What structure creates maximum clarity and impact?",
        "section_id": 7, "question_type": "SCENARIO", "class_min": 11, "class_max": 12, "difficulty": "Medium",
        "skill_category": "communication", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Problem-Solution-Impact structure delivers compelling synthesis under tight executive constraints.",
        "options": [
            {"option_text": "Spend 2.5 minutes on personal introductions and greeting pleasantries", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "State the core problem, present the validated solution, and demonstrate measurable impact and budget needs", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Read every word from a 50-bullet-point dense slide deck", "option_value": "C", "score": 0.1, "is_correct": False, "display_order": 3},
            {"option_text": "Refuse to give a presentation without written approval", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 8: CREATIVITY (Section ID: 8)
    # ========================================================
    {
        "question_code": "CREAT_01_ALT_78",
        "question_text": "When given an everyday object like an empty plastic bottle, how often do you envision transforming it into something new (bird feeder, planter, science model)?",
        "section_id": 8, "question_type": "RATING", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "creativity", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Measures spontaneous lateral thinking and divergent ideation.",
        "options": make_rating_options("Never Think of Crafts", "Constantly Repurposing & Prototyping")
    },
    {
        "question_code": "CREAT_02_DESIGN_910",
        "question_text": "Scenario: Design a mobile app interface for elderly users with low eyesight. Which creative feature solves the core challenge best?",
        "section_id": 8, "question_type": "SCENARIO", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "creativity", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Human-centered creative design prioritizes high-contrast typography, intuitive voice commands, and minimal cognitive load.",
        "options": [
            {"option_text": "Add complex animated 3D particle effects and small text", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Implement high-contrast typography, intuitive voice-guided commands, and large tactile touch zones", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Hide all buttons inside nested multi-level menus", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Remove color entirely from the screen", "option_value": "D", "score": 0.2, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "CREAT_03_SYNTH_1112",
        "question_text": "How often do you blend concepts from completely different fields (e.g. applying biological biomimicry to architectural design or music to coding)?",
        "section_id": 8, "question_type": "RATING", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "creativity", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Cross-domain synthesis is the highest hallmark of transformative creative problem solving.",
        "options": make_rating_options("Never Synthesize", "Constantly Design Interdisciplinary Concepts")
    },

    # ========================================================
    # SECTION 9: DIGITAL ABILITY (Section ID: 9)
    # ========================================================
    {
        "question_code": "DIG_01_SEC_78",
        "question_text": "You receive an email claiming you won an iPhone and asking you to click an unknown link and enter your parent's phone number. What should you do?",
        "section_id": 9, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "digital_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Recognizing phishing attempts and suspicious links is fundamental to cyber safety.",
        "options": [
            {"option_text": "Click the link immediately to claim the prize", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Forward the email to all school friends", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "Do not click, flag the email as phishing / spam, and alert an adult", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "Reply asking for two iPhones instead of one", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "DIG_02_ALGO_910",
        "question_text": "What is the output of the following logic loop: count = 0; for i from 1 to 4 do count = count + i; print(count)?",
        "section_id": 9, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "digital_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Iteration: i=1 -> 1; i=2 -> 1+2=3; i=3 -> 3+3=6; i=4 -> 6+4=10.",
        "options": [
            {"option_text": "4", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "8", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "10", "option_value": "C", "score": 1.0, "is_correct": True, "display_order": 3},
            {"option_text": "14", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "DIG_03_DB_910",
        "question_text": "In a relational database for a school, which field serves best as a Unique Primary Key for identifying each student?",
        "section_id": 9, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "digital_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "A Student Admission / Roll Number is strictly unique, whereas first names, birth cities, and grades can have duplicates.",
        "options": [
            {"option_text": "Student First Name", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Student Admission ID / Roll Number", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Grade / Class Level", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Favorite Color", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "DIG_04_AI_1112",
        "question_text": "How does a Machine Learning classification model differ fundamentally from a traditional rule-based software program?",
        "section_id": 9, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "digital_ability", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "Traditional programming executes human-coded IF-THEN rules; ML algorithms learn patterns, weights, and decision boundaries directly from training data.",
        "options": [
            {"option_text": "ML requires no computer hardware to run", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "ML learns statistical patterns and weights from data rather than relying solely on explicit hardcoded rules", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Rule-based programs are always 100% inaccurate", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "There is no difference between ML and traditional programming", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 10: LEARNING ABILITY (Section ID: 10)
    # ========================================================
    {
        "question_code": "LEARN_01_NEW_78",
        "question_text": "When you encounter a completely new or confusing topic in class, what is your usual reaction?",
        "section_id": 10, "question_type": "SCENARIO", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Active learning resilience involves asking clarifying questions and seeking conceptual mastery.",
        "options": [
            {"option_text": "Give up and ignore the subject", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Ask questions, look up examples, and practice until the concept clicks", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Wait for exam day to guess answers", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Blame the textbook author", "option_value": "D", "score": 0.1, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LEARN_02_AUTON_910",
        "question_text": "How comfortable are you learning a new skill independently using online tutorials, documentation, or books without formal classroom supervision?",
        "section_id": 10, "question_type": "RATING", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Self-directed learning autonomy is a critical predictor for higher education success.",
        "options": make_rating_options("Need Constant Supervision", "Thrive on Independent Deep Research")
    },
    {
        "question_code": "LEARN_03_ADAPT_1112",
        "question_text": "When a strategy you relied on for years stops producing top results in advanced coursework, how rapidly do you adapt and adopt new mental models?",
        "section_id": 10, "question_type": "RATING", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Metacognitive adaptability measures agility in unlearning ineffective strategies.",
        "options": make_rating_options("Resist Change", "Rapidly Self-Optimize & Adapt")
    },

    # ========================================================
    # SECTION 11: SPATIAL ABILITY (Section ID: 11)
    # ========================================================
    {
        "question_code": "SPAT_01_CUBE_910",
        "question_text": "If a solid cube is painted blue on all 6 faces and then cut into 27 equal smaller cubes (3x3x3), how many small cubes have exactly 2 blue faces?",
        "section_id": 11, "question_type": "MCQ", "class_min": 7, "class_max": 10, "difficulty": "Medium",
        "skill_category": "spatial_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Cubes with 2 painted faces lie along the 12 edges (excluding corners). For 3x3x3, each of the 12 edges has 1 middle cube -> 12 cubes.",
        "options": [
            {"option_text": "8", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "12", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "16", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "24", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SPAT_02_FOLD_910",
        "question_text": "When a flat cross-shaped cardboard net with 6 numbered squares is folded into a cube, which faces are always opposite to each other?",
        "section_id": 11, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "spatial_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "In an unfolded cube net, faces separated by exactly one intervening square fold into opposite parallel faces.",
        "options": [
            {"option_text": "Faces separated by one intervening square in a straight line", "option_value": "A", "score": 1.0, "is_correct": True, "display_order": 1},
            {"option_text": "Any two adjacent corner squares", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "The top and left-most tabs only", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Faces cannot be predicted without folding physically", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "SPAT_03_GEAR_1112",
        "question_text": "Gear A (with 20 teeth) rotates clockwise at 100 RPM and drives Gear B (with 40 teeth), which in turn drives Gear C (with 10 teeth). In which direction and speed does Gear C rotate?",
        "section_id": 11, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "spatial_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "A (Clockwise) -> B (Counter-clockwise) -> C (Clockwise). Speed = 100 * (20/10) = 200 RPM Clockwise.",
        "options": [
            {"option_text": "Counter-clockwise at 50 RPM", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Clockwise at 200 RPM", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Counter-clockwise at 200 RPM", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Clockwise at 100 RPM", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 12: PRACTICAL ABILITY (Section ID: 12)
    # ========================================================
    {
        "question_code": "PRAC_01_LEVER_910",
        "question_text": "To lift a heavy 100 kg stone with a rigid metal crowbar, where should the pivot fulcrum be placed to require the minimum lifting effort?",
        "section_id": 12, "question_type": "MCQ", "class_min": 7, "class_max": 10, "difficulty": "Easy",
        "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Placing the fulcrum close to the heavy load maximizes the mechanical advantage (Effort Arm > Load Arm).",
        "options": [
            {"option_text": "As close as possible to the heavy stone (load)", "option_value": "A", "score": 1.0, "is_correct": True, "display_order": 1},
            {"option_text": "Exactly in the middle of the crowbar", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "Right under your hands (effort point)", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Fulcrum placement does not affect required force", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PRAC_02_TOOL_910",
        "question_text": "Which precision measurement tool is best suited for measuring the exact internal diameter of a small engine cylinder or pipe?",
        "section_id": 12, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Vernier calipers have dedicated inside jaws designed for high-precision internal diameter measurement.",
        "options": [
            {"option_text": "Standard wooden meter ruler", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Vernier Caliper with internal measurement jaws", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Flexible tailor's measuring tape", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Protractor", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PRAC_03_DIAG_1112",
        "question_text": "Scenario: A 12V DC cooling fan in an electronic device is not spinning. A multimeter shows 12V across the power terminals. What is the most likely diagnosis?",
        "section_id": 12, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Since full operating voltage is present at the terminals, the external power supply is working and the internal fan motor windings or bearings have failed.",
        "options": [
            {"option_text": "The main wall power outlet is disconnected", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "The fan motor internal coil is open-circuited or mechanically seized", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "The multimeter battery is low", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "The electrical polarity reversed itself naturally", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 13: INTERESTS (Section ID: 13) - 23 Dimensions
    # ========================================================
    {"question_code": "INT_MATH", "question_text": "How interested are you in mathematics, quantitative equations, and financial models?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 1, "explanation": "Mathematics interest.", "options": make_rating_options()},
    {"question_code": "INT_SCI", "question_text": "How interested are you in physics, space exploration, and scientific research?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "science_interest", "stream_specific": "All", "is_required": True, "display_order": 2, "explanation": "Science interest.", "options": make_rating_options()},
    {"question_code": "INT_TECH", "question_text": "How interested are you in computer programming, artificial intelligence, and digital apps?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "technology_interest", "stream_specific": "All", "is_required": True, "display_order": 3, "explanation": "Technology interest.", "options": make_rating_options()},
    {"question_code": "INT_MED", "question_text": "How interested are you in medicine, surgery, healthcare clinics, and curing illnesses?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "healthcare_interest", "stream_specific": "All", "is_required": True, "display_order": 4, "explanation": "Healthcare interest.", "options": make_rating_options()},
    {"question_code": "INT_ENG", "question_text": "How interested are you in mechanical engines, robotics, building structures, and engineering?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 5, "explanation": "Engineering interest.", "options": make_rating_options()},
    {"question_code": "INT_BUS", "question_text": "How interested are you in business startups, commercial entrepreneurship, and corporate leadership?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "business_interest", "stream_specific": "All", "is_required": True, "display_order": 6, "explanation": "Business interest.", "options": make_rating_options()},
    {"question_code": "INT_FIN", "question_text": "How interested are you in stock markets, banking, corporate finance, and wealth investment?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "business_interest", "stream_specific": "All", "is_required": True, "display_order": 7, "explanation": "Finance interest.", "options": make_rating_options()},
    {"question_code": "INT_LAW", "question_text": "How interested are you in constitutional law, legal defense, courtroom justice, and advocacy?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "social_interest", "stream_specific": "All", "is_required": True, "display_order": 8, "explanation": "Law interest.", "options": make_rating_options()},
    {"question_code": "INT_EDU", "question_text": "How interested are you in teaching, academic mentoring, student counseling, and education?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "social_interest", "stream_specific": "All", "is_required": True, "display_order": 9, "explanation": "Education interest.", "options": make_rating_options()},
    {"question_code": "INT_PSY", "question_text": "How interested are you in human psychology, mental health, cognitive therapy, and behavior?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "social_interest", "stream_specific": "All", "is_required": True, "display_order": 10, "explanation": "Psychology interest.", "options": make_rating_options()},
    {"question_code": "INT_ART", "question_text": "How interested are you in fine arts, painting, illustration, and sculpture?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "creative_interest", "stream_specific": "All", "is_required": True, "display_order": 11, "explanation": "Arts interest.", "options": make_rating_options()},
    {"question_code": "INT_DES", "question_text": "How interested are you in UI/UX design, graphic design, interior decor, and architecture?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "creative_interest", "stream_specific": "All", "is_required": True, "display_order": 12, "explanation": "Design interest.", "options": make_rating_options()},
    {"question_code": "INT_WRITE", "question_text": "How interested are you in creative writing, journalism, literature, and blogging?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "communication", "stream_specific": "All", "is_required": True, "display_order": 13, "explanation": "Writing interest.", "options": make_rating_options()},
    {"question_code": "INT_MEDIA", "question_text": "How interested are you in filmmaking, digital media, photography, broadcasting, and podcasting?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "creative_interest", "stream_specific": "All", "is_required": True, "display_order": 14, "explanation": "Media interest.", "options": make_rating_options()},
    {"question_code": "INT_SPT", "question_text": "How interested are you in athletics, competitive team sports, fitness training, and sports science?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 15, "explanation": "Sports interest.", "options": make_rating_options()},
    {"question_code": "INT_NAT", "question_text": "How interested are you in wildlife protection, animal care, biology reserves, and forestry?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "science_interest", "stream_specific": "All", "is_required": True, "display_order": 16, "explanation": "Nature interest.", "options": make_rating_options()},
    {"question_code": "INT_RES", "question_text": "How interested are you in academic research, laboratory experiments, and publishing breakthroughs?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "research_interest", "stream_specific": "All", "is_required": True, "display_order": 17, "explanation": "Research interest.", "options": make_rating_options()},
    {"question_code": "INT_SOC", "question_text": "How interested are you in community development, charity volunteering, and NGO public service?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "social_interest", "stream_specific": "All", "is_required": True, "display_order": 18, "explanation": "Social service interest.", "options": make_rating_options()},
    {"question_code": "INT_AVI", "question_text": "How interested are you in aerospace engineering, drones, and aircraft piloting?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 19, "explanation": "Aviation interest.", "options": make_rating_options()},
    {"question_code": "INT_AGR", "question_text": "How interested are you in modern agriculture, crop sciences, soil agronomy, and organic farming?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "science_interest", "stream_specific": "All", "is_required": True, "display_order": 20, "explanation": "Agriculture interest.", "options": make_rating_options()},
    {"question_code": "INT_ENV", "question_text": "How interested are you in climate change solutions, renewable solar/wind energy, and sustainability?", "section_id": 13, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "science_interest", "stream_specific": "All", "is_required": True, "display_order": 21, "explanation": "Environment interest.", "options": make_rating_options()},

    # ========================================================
    # SECTION 14: ACTIVITIES (Section ID: 14) - 14 Dimensions
    # ========================================================
    {"question_code": "ACT_CODE", "question_text": "How often do you write computer code, build scripts, or create digital web/app projects?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "digital_ability", "stream_specific": "All", "is_required": True, "display_order": 1, "explanation": "Coding activity.", "options": make_frequency_options()},
    {"question_code": "ACT_ROBOT", "question_text": "How often do you assemble electronics kits, Arduino/Raspberry Pi projects, or robotics models?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 2, "explanation": "Robotics maker activity.", "options": make_frequency_options()},
    {"question_code": "ACT_SCICLUB", "question_text": "How often do you conduct science experiments or participate in school science club exhibitions?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "scientific_reasoning", "stream_specific": "All", "is_required": True, "display_order": 3, "explanation": "Science club activity.", "options": make_frequency_options()},
    {"question_code": "ACT_MATHCLUB", "question_text": "How often do you practice competitive math Olympiad problems, logic puzzles, or Sudoku?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "mathematical_ability", "stream_specific": "All", "is_required": True, "display_order": 4, "explanation": "Math club activity.", "options": make_frequency_options()},
    {"question_code": "ACT_DEBATE", "question_text": "How often do you participate in debates, Model UN, public speaking, or student declamations?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "communication", "stream_specific": "All", "is_required": True, "display_order": 5, "explanation": "Debate activity.", "options": make_frequency_options()},
    {"question_code": "ACT_DRAMA", "question_text": "How often do you act in school theater plays, musical performances, or dramatic storytelling?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "creativity", "stream_specific": "All", "is_required": True, "display_order": 6, "explanation": "Drama & performing arts activity.", "options": make_frequency_options()},
    {"question_code": "ACT_ART", "question_text": "How often do you sketch, paint, design digital artwork, or create craft models?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "creativity", "stream_specific": "All", "is_required": True, "display_order": 7, "explanation": "Art & design activity.", "options": make_frequency_options()},
    {"question_code": "ACT_MUSIC", "question_text": "How often do you play a musical instrument, compose music, or sing?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "creativity", "stream_specific": "All", "is_required": True, "display_order": 8, "explanation": "Music activity.", "options": make_frequency_options()},
    {"question_code": "ACT_SPORTS", "question_text": "How often do you participate in competitive outdoor team sports or athletic fitness training?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 9, "explanation": "Sports activity.", "options": make_frequency_options()},
    {"question_code": "ACT_READING", "question_text": "How often do you read non-fiction books, industry blogs, science magazines, or news journals?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 10, "explanation": "Reading activity.", "options": make_frequency_options()},
    {"question_code": "ACT_PHOTO", "question_text": "How often do you practice photography, video editing, or visual media production?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "creative_interest", "stream_specific": "All", "is_required": True, "display_order": 11, "explanation": "Photography activity.", "options": make_frequency_options()},
    {"question_code": "ACT_VOLUNTEER", "question_text": "How often do you volunteer for community social service, cleanliness drives, or charity work?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "social_interest", "stream_specific": "All", "is_required": True, "display_order": 12, "explanation": "Volunteering activity.", "options": make_frequency_options()},
    {"question_code": "ACT_ENTREP", "question_text": "How often do you brainstorm business startup ideas, organize bake sales, or plan monetization projects?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "business_interest", "stream_specific": "All", "is_required": True, "display_order": 13, "explanation": "Entrepreneurship activity.", "options": make_frequency_options()},
    {"question_code": "ACT_WRITING", "question_text": "How often do you write personal essays, articles, poems, or stories outside school requirements?", "section_id": 14, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy", "skill_category": "communication", "stream_specific": "All", "is_required": True, "display_order": 14, "explanation": "Creative writing activity.", "options": make_frequency_options()},

    # ========================================================
    # SECTION 15: TEAMWORK (Section ID: 15)
    # ========================================================
    {
        "question_code": "TEAM_01_DISP_78",
        "question_text": "Scenario: During a group project, two teammates strongly disagree on the poster design. How do you resolve this?",
        "section_id": 15, "question_type": "SCENARIO", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "teamwork", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Collaborative compromise harmonizes multiple viewpoints constructively.",
        "options": [
            {"option_text": "Pick the loudest person's idea to end the argument quickly", "option_value": "A", "score": 0.2, "is_correct": False, "display_order": 1},
            {"option_text": "Listen to both ideas, find common ground, and combine the best elements of both", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Tell both to leave the group and work completely alone", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Complain to the principal immediately", "option_value": "D", "score": 0.1, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "TEAM_02_DEADLINE_910",
        "question_text": "Scenario: A teammate is falling behind on their assigned part of a project due to illness. How should the team respond?",
        "section_id": 15, "question_type": "SCENARIO", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "teamwork", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "High-performing teams exhibit mutual support and dynamic workload reallocation.",
        "options": [
            {"option_text": "Remove their name from the project without asking", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Check in empathetically, redistribute manageable tasks among remaining members, and support them", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Ignore their incomplete section and submit partial work", "option_value": "C", "score": 0.1, "is_correct": False, "display_order": 3},
            {"option_text": "Wait until the last minute and panic", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "TEAM_03_CROSS_1112",
        "question_text": "Scenario: In a multidisciplinary team (engineers, designers, marketers), differing technical jargons create friction. What is the best team intervention?",
        "section_id": 15, "question_type": "SCENARIO", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "teamwork", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Establishing shared project milestones and plain language cross-functional alignment bridges disciplinary silos.",
        "options": [
            {"option_text": "Demand that designers learn engineering code immediately", "option_value": "A", "score": 0.1, "is_correct": False, "display_order": 1},
            {"option_text": "Establish a shared project glossary, align on unified customer outcomes, and schedule weekly cross-review syncs", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Split into completely isolated groups with zero communication", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Let the loudest department make all decisions", "option_value": "D", "score": 0.1, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 16: LEADERSHIP (Section ID: 16)
    # ========================================================
    {
        "question_code": "LEAD_01_INIT_78",
        "question_text": "Scenario: Your teacher asks the class to organize a classroom clean-up drive, but no one is stepping forward. What do you do?",
        "section_id": 16, "question_type": "SCENARIO", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "leadership", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Leadership begins with initiative and inviting collaborative peer participation.",
        "options": [
            {"option_text": "Wait quietly for someone else to act", "option_value": "A", "score": 0.2, "is_correct": False, "display_order": 1},
            {"option_text": "Step up, volunteer to start, and encourage friends to take small specific roles", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Leave the classroom", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Complain that clean-up is boring", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LEAD_02_DELEG_910",
        "question_text": "Scenario: As captain of a school event, you have 4 major tasks to complete. How should you assign responsibilities?",
        "section_id": 16, "question_type": "SCENARIO", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "leadership", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Effective leaders match individual strengths to tasks and provide clear support.",
        "options": [
            {"option_text": "Do all 4 tasks entirely by yourself to maintain total control", "option_value": "A", "score": 0.2, "is_correct": False, "display_order": 1},
            {"option_text": "Match tasks to members' individual strengths, define clear outcomes, and empower them with trust", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Assign tasks randomly by drawing chits", "option_value": "C", "score": 0.2, "is_correct": False, "display_order": 3},
            {"option_text": "Order people around without helping", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "LEAD_03_ETHIC_1112",
        "question_text": "Scenario: Your team discovers a minor calculation error in a contest submission that gave you an unfair winning score. What leadership action do you take?",
        "section_id": 16, "question_type": "SCENARIO", "class_min": 11, "class_max": 12, "difficulty": "Hard",
        "skill_category": "leadership", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Integrity and ethical transparency under pressure define genuine leadership character.",
        "options": [
            {"option_text": "Hide the error and pretend nothing happened", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Notify the judges transparently, explain the calculation correction, and accept the rightful outcome", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Blame the junior teammate who typed the numbers", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Argue with the organizers", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 17: WORK PREFERENCES (Section ID: 17)
    # ========================================================
    {
        "question_code": "WORK_01_ENV",
        "question_text": "Which physical work environment appeals most to your ideal day-to-day lifestyle?",
        "section_id": 17, "question_type": "MCQ", "class_min": 7, "class_max": 12, "difficulty": "Easy",
        "skill_category": "practical_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Physical workplace preference mapping.",
        "options": [
            {"option_text": "Modern technology office / Creative studio / Tech hub", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Scientific laboratory / Hospital / Medical diagnostic clinic", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Outdoor field sites / Ecological reserves / Construction infrastructure", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Flexible remote home office / Global digital nomad lifestyle", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "WORK_02_STYLE",
        "question_text": "Do you prefer deep, focused, independent work or highly interactive, people-facing collaboration?",
        "section_id": 17, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy",
        "skill_category": "communication", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Independent analysis vs interpersonal collaboration continuum.",
        "options": make_rating_options("100% Solo Independent Focus", "Constant Collaborative Engagement")
    },
    {
        "question_code": "WORK_03_DATA_PEOPLE",
        "question_text": "Do you feel more energized working with code, numbers, and machines, or interacting directly with clients, patients, and audiences?",
        "section_id": 17, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy",
        "skill_category": "communication", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Data/Technology orientation vs People-facing orientation.",
        "options": make_rating_options("Strictly Data & Code", "Strictly People & Social Interaction")
    },
    {
        "question_code": "WORK_04_TRAVEL",
        "question_text": "How appealing is frequent domestic or international professional travel to you?",
        "section_id": 17, "question_type": "RATING", "class_min": 7, "class_max": 12, "difficulty": "Easy",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "Travel and mobility preference.",
        "options": make_rating_options("Zero Travel (Stable Location)", "Frequent National/Global Travel")
    },

    # ========================================================
    # SECTION 18: CAREER AWARENESS (Section ID: 18)
    # ========================================================
    {
        "question_code": "AWARE_01_ROLES_78",
        "question_text": "Which career role is primarily responsible for ensuring airplanes fly safely along predetermined flight paths and altitudes?",
        "section_id": 18, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "observation", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Air Traffic Controllers coordinate aircraft movements and navigation corridors.",
        "options": [
            {"option_text": "Mechanical Automobile Fitter", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Air Traffic Controller / Flight Pilot", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Architectural Land Surveyor", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Chartered Accountant", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "AWARE_02_STUDY_78",
        "question_text": "If a student loves both biology and computer coding, which exciting modern interdisciplinary field blends both?",
        "section_id": 18, "question_type": "MCQ", "class_min": 7, "class_max": 8, "difficulty": "Easy",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Bioinformatics and Computational Biology merge genetic biology with computer algorithms.",
        "options": [
            {"option_text": "Bioinformatics & Computational Biology", "option_value": "A", "score": 1.0, "is_correct": True, "display_order": 1},
            {"option_text": "Civil Structural Masonry", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "Corporate Tax Law", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Classical History Archaeology", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "AWARE_03_TRENDS_910",
        "question_text": "Which combination of emerging fields is creating significant new cross-disciplinary careers globally?",
        "section_id": 18, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Artificial Intelligence, Renewable Green Energy, and Genomic Biotechnology represent high-growth 21st-century frontiers.",
        "options": [
            {"option_text": "Typewriter assembly and telegraph transmission", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "Artificial Intelligence, Renewable Energy & Genomic Biotechnology", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "Manual film reel developing", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "Steam locomotive stoking", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "AWARE_04_STREAMS_910",
        "question_text": "Which higher secondary stream provides the mandatory foundational subject requirements for pursuing a Bachelor of Architecture (B.Arch)?",
        "section_id": 18, "question_type": "MCQ", "class_min": 9, "class_max": 10, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 4,
        "explanation": "B.Arch admission councils mandate Physics, Chemistry, and Mathematics (PCM) with qualifying entrance exams (NATA / JEE Main Paper 2).",
        "options": [
            {"option_text": "Science stream with Mathematics and Physics", "option_value": "A", "score": 1.0, "is_correct": True, "display_order": 1},
            {"option_text": "Commerce without Mathematics", "option_value": "B", "score": 0.0, "is_correct": False, "display_order": 2},
            {"option_text": "Pure Literature and Languages only", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "No formal school prerequisites are required", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "AWARE_05_DEG_1112",
        "question_text": "Which degree or professional qualification is directly required to practice as an advocate in court?",
        "section_id": 18, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 5,
        "explanation": "An LL.B. (Bachelor of Laws) or integrated B.A./B.B.A. LL.B. accredited by the Bar Council is mandatory for legal practice.",
        "options": [
            {"option_text": "B.Tech Computer Science", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "LL.B. (Bachelor of Laws) + Bar Council Enrollment", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "MBBS (Bachelor of Medicine)", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "B.Com General Accounting", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "AWARE_06_EXAMS_1112",
        "question_text": "Which competitive entrance exam is the primary national gateway for admission to undergraduate medical (MBBS/BDS) programs across India?",
        "section_id": 18, "question_type": "MCQ", "class_min": 11, "class_max": 12, "difficulty": "Easy",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 6,
        "explanation": "NEET-UG (National Eligibility cum Entrance Test) is the standardized national medical gateway.",
        "options": [
            {"option_text": "JEE Advanced", "option_value": "A", "score": 0.0, "is_correct": False, "display_order": 1},
            {"option_text": "NEET-UG", "option_value": "B", "score": 1.0, "is_correct": True, "display_order": 2},
            {"option_text": "CLAT", "option_value": "C", "score": 0.0, "is_correct": False, "display_order": 3},
            {"option_text": "CAT", "option_value": "D", "score": 0.0, "is_correct": False, "display_order": 4}
        ]
    },

    # ========================================================
    # SECTION 19: CAREER PREFERENCES (Section ID: 19)
    # ========================================================
    {
        "question_code": "PREF_01_PRIMARY",
        "question_text": "Which broad industry sector currently represents your highest aspirational career goal?",
        "section_id": 19, "question_type": "MCQ", "class_min": 7, "class_max": 12, "difficulty": "Easy",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 1,
        "explanation": "Primary student career preference capture.",
        "options": [
            {"option_text": "Technology, Software & Artificial Intelligence", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Healthcare, Medicine, Nursing & Biotechnology", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Engineering, Robotics, Aviation & Architecture", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Business, Finance, Law, Civil Services & Creative Media", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PREF_02_GOAL",
        "question_text": "When thinking about your career 10 years after college, what type of professional impact matters most to you?",
        "section_id": 19, "question_type": "MCQ", "class_min": 7, "class_max": 12, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 2,
        "explanation": "Long-term intrinsic motivation and career values orientation.",
        "options": [
            {"option_text": "Innovating breakthrough technological inventions or software products", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Healing patients, saving lives, and advancing health research", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Leading high-growth commercial enterprises and driving business strategy", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "Serving the public, upholding justice, creating art, or educating future generations", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    },
    {
        "question_code": "PREF_03_SECTOR",
        "question_text": "Which organizational structure aligns closest with your working aspirations?",
        "section_id": 19, "question_type": "MCQ", "class_min": 9, "class_max": 12, "difficulty": "Medium",
        "skill_category": "learning_ability", "stream_specific": "All", "is_required": True, "display_order": 3,
        "explanation": "Sector preference (Public vs Private Corporate vs Startup Entrepreneurship vs Academia).",
        "options": [
            {"option_text": "Fast-paced Tech Startup / Entrepreneurship Venture", "option_value": "A", "score": 1.0, "is_correct": False, "display_order": 1},
            {"option_text": "Established Global Corporation / Multinational Enterprise", "option_value": "B", "score": 1.0, "is_correct": False, "display_order": 2},
            {"option_text": "Civil Services / Public Governance / Defense Forces", "option_value": "C", "score": 1.0, "is_correct": False, "display_order": 3},
            {"option_text": "University Research Lab / Creative Independent Practice", "option_value": "D", "score": 1.0, "is_correct": False, "display_order": 4}
        ]
    }
]


def export_questions_to_json():
    """Saves master questions to database/questions_seed.json."""
    json_path = BASE_DIR / 'database' / 'questions_seed.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(MASTER_QUESTIONS, f, indent=2)
    print(f"Exported {len(MASTER_QUESTIONS)} questions to {json_path.name}")


def export_questions_to_sql():
    """Generates database/questions_seed.sql for MySQL Workbench."""
    sql_path = BASE_DIR / 'database' / 'questions_seed.sql'
    statements = [
        "-- ============================================================",
        "-- Adaptive Student Question Bank - MySQL Workbench SQL Script",
        "-- Contains questions across all 19 standardized assessment sections",
        "-- ============================================================",
        "USE `career_recommendation_db`;\n",
        "SET FOREIGN_KEY_CHECKS = 0;\n",
        "DELETE FROM `question_options`;",
        "DELETE FROM `questions`;\n"
    ]

    q_id = 1
    opt_id = 1
    for q in MASTER_QUESTIONS:
        q_text = q['question_text'].replace("'", "''")
        expl = (q.get('explanation') or '').replace("'", "''")
        stream = q.get('stream_specific', 'All')

        statements.append(
            f"INSERT INTO `questions` (`id`, `question_code`, `question_text`, `section_id`, `question_type`, "
            f"`class_min`, `class_max`, `difficulty`, `skill_category`, `stream_specific`, `is_required`, `display_order`, `explanation`, `is_active`) "
            f"VALUES ({q_id}, '{q['question_code']}', '{q_text}', {q['section_id']}, '{q['question_type']}', "
            f"{q['class_min']}, {q['class_max']}, '{q['difficulty']}', '{q['skill_category']}', '{stream}', TRUE, {q['display_order']}, '{expl}', TRUE);"
        )

        for opt in q.get('options', []):
            o_text = opt['option_text'].replace("'", "''")
            o_val = str(opt['option_value']).replace("'", "''")
            is_corr = 1 if opt.get('is_correct') else 0
            score = float(opt.get('score', 0.0))

            statements.append(
                f"INSERT INTO `question_options` (`id`, `question_id`, `option_text`, `option_value`, `score`, `is_correct`, `display_order`) "
                f"VALUES ({opt_id}, {q_id}, '{o_text}', '{o_val}', {score}, {is_corr}, {opt['display_order']});"
            )
            opt_id += 1

        q_id += 1

    statements.append("\nSET FOREIGN_KEY_CHECKS = 1;\n")

    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(statements))
    print(f"Generated {sql_path.name} ({sql_path.stat().st_size / 1024:.1f} KB)")


def seed_questions_into_mysql():
    """Inserts all questions and options into the live MySQL database idempotently."""
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', 'abc123')
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    db_name = os.getenv('DB_NAME', 'career_recommendation_db')

    print(f"Connecting to MySQL Server on {host}:{port} -> Database: {db_name}...")
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=db_name,
        autocommit=False
    )
    cursor = conn.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("DELETE FROM question_options;")
        cursor.execute("DELETE FROM questions;")

        q_count = 0
        opt_count = 0

        for q in MASTER_QUESTIONS:
            cursor.execute(
                """
                INSERT INTO questions (
                    question_code, question_text, section_id, question_type,
                    class_min, class_max, difficulty, skill_category, stream_specific,
                    is_required, display_order, explanation, is_active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE);
                """,
                (
                    q['question_code'], q['question_text'], q['section_id'], q['question_type'],
                    q['class_min'], q['class_max'], q['difficulty'], q['skill_category'],
                    q.get('stream_specific', 'All'), q['is_required'], q['display_order'],
                    q.get('explanation')
                )
            )
            q_id = cursor.lastrowid
            q_count += 1

            for opt in q.get('options', []):
                cursor.execute(
                    """
                    INSERT INTO question_options (
                        question_id, option_text, option_value, score, is_correct, display_order
                    ) VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        q_id, opt['option_text'], str(opt['option_value']),
                        float(opt.get('score', 0.0)), bool(opt.get('is_correct', False)),
                        int(opt['display_order'])
                    )
                )
                opt_count += 1

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print(f"[OK] Successfully seeded {q_count} questions and {opt_count} options into MySQL Server!")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Seeding failed: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    export_questions_to_json()
    export_questions_to_sql()
    seed_questions_into_mysql()
