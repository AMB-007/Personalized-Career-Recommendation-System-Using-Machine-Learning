"""
Generate High-Resolution Publication-Quality Sequence Diagrams for Database Architecture Report.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "database"

def generate_database_sequence_diagram():
    fig, ax = plt.subplots(figsize=(16, 20), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Lifeline definitions (x-coordinates and labels)
    lifelines = [
        {"x": 1.2, "name": "Student Client\n(Web UI / SPA)", "color": "#0ea5e9"},
        {"x": 4.0, "name": "Flask App Gateway\n(Routes & Auth)", "color": "#6366f1"},
        {"x": 6.8, "name": "MySQL: User & Profile\n(users, students, marks)", "color": "#10b981"},
        {"x": 9.6, "name": "MySQL: Assessment Core\n(questions, sessions, answers)", "color": "#f59e0b"},
        {"x": 12.4, "name": "ML Inference Engine\n(Scoring & CatBoost V9.5)", "color": "#ec4899"},
        {"x": 15.0, "name": "MySQL: Recs & Careers\n(careers, pathways, recs)", "color": "#8b5cf6"}
    ]

    total_height = 28
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, total_height)
    ax.axis('off')

    # Draw Title Header
    ax.text(8.0, 27.2, "DATABASE TRANSACTION & ML INFERENCE SEQUENCE DIAGRAM", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0f172a')
    ax.text(8.0, 26.6, "End-to-End ACID Transaction Lifecycle from Student Onboarding to CatBoost Model Recommendations", 
            ha='center', va='center', fontsize=10, color='#64748b', style='italic')

    # Draw Lifelines Header Boxes and Vertical Lines
    for ll in lifelines:
        x = ll["x"]
        # Header box
        box = patches.FancyBboxPatch((x - 1.0, 24.8), 2.0, 1.3, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     edgecolor=ll["color"], facecolor=ll["color"], alpha=0.95, zorder=3)
        ax.add_patch(box)
        ax.text(x, 25.45, ll["name"], ha='center', va='center', fontsize=8.5, fontweight='bold', color='#ffffff', zorder=4)

        # Vertical dashed lifeline
        ax.plot([x, x], [1.5, 24.8], color='#cbd5e1', linestyle='--', linewidth=1.2, zorder=1)

        # Footer box
        box_bot = patches.FancyBboxPatch((x - 0.9, 0.6), 1.8, 0.8, boxstyle="round,pad=0.1,rounding_size=0.2",
                                         edgecolor=ll["color"], facecolor='#f8fafc', linewidth=1.2, zorder=3)
        ax.add_patch(box_bot)
        ax.text(x, 1.0, ll["name"].split('\n')[0], ha='center', va='center', fontsize=7.5, fontweight='bold', color='#334155', zorder=4)

    # Sequence Messages & Actions
    # y coordinates decrement from 24 down to 2
    steps = [
        # PHASE 1: REGISTRATION & ONBOARDING
        {"type": "phase", "y": 24.0, "title": "PHASE 1: REGISTRATION & MANDATORY ACADEMIC MARKS ONBOARDING"},
        {"type": "call", "y": 23.1, "from": 1.2, "to": 4.0, "text": "1. POST /register (Name, Email, Password, Grade, Board)", "color": "#0284c7"},
        {"type": "call", "y": 22.3, "from": 4.0, "to": 6.8, "text": "2. BEGIN TRANSACTION -> INSERT INTO users, students, academic_scores (NULL)", "color": "#059669"},
        {"type": "return", "y": 21.6, "from": 6.8, "to": 4.0, "text": "3. COMMIT -> Return student_id & user_id", "color": "#059669"},
        {"type": "return", "y": 20.9, "from": 4.0, "to": 1.2, "text": "4. 302 Redirect to /profile?onboarding=1 (Prompt for 17 Subject Marks)", "color": "#4f46e5"},
        {"type": "call", "y": 20.1, "from": 1.2, "to": 4.0, "text": "5. POST /profile (Dynamic Marks: Math, Science, Physics, Bio, CS, etc.)", "color": "#0284c7"},
        {"type": "call", "y": 19.3, "from": 4.0, "to": 6.8, "text": "6. UPDATE academic_scores SET math=..., bio=..., overall_percentage=...", "color": "#059669"},
        {"type": "return", "y": 18.6, "from": 6.8, "to": 1.2, "text": "7. COMMIT -> Profile Validated & Ready for Assessment", "color": "#059669"},

        # PHASE 2: ADAPTIVE ASSESSMENT SESSION
        {"type": "phase", "y": 17.8, "title": "PHASE 2: ADAPTIVE ASSESSMENT INITIALIZATION & REAL-TIME AUTOSAVE"},
        {"type": "call", "y": 16.9, "from": 1.2, "to": 4.0, "text": "8. GET /assessment/start (Check is_academic_profile_complete() == True)", "color": "#0284c7"},
        {"type": "call", "y": 16.1, "from": 4.0, "to": 9.6, "text": "9. INSERT INTO assessment_sessions (status='in_progress', selected_question_ids)", "color": "#d97706"},
        {"type": "call", "y": 15.3, "from": 4.0, "to": 9.6, "text": "10. SELECT questions JOIN question_options WHERE class_min <= class <= class_max", "color": "#d97706"},
        {"type": "return", "y": 14.5, "from": 9.6, "to": 1.2, "text": "11. 200 OK -> Render Assessment UI with Dynamic Question Palette", "color": "#4f46e5"},
        {"type": "call", "y": 13.7, "from": 1.2, "to": 9.6, "text": "12. POST /api/assessment/answer (Autosave: student_answers UPSERT)", "color": "#d97706", "dashed": True},
        {"type": "return", "y": 13.0, "from": 9.6, "to": 1.2, "text": "13. UPDATE assessment_sessions SET completion_percentage = X%", "color": "#d97706", "dashed": True},

        # PHASE 3: SUBMISSION & ML INFERENCE PIPELINE
        {"type": "phase", "y": 12.2, "title": "PHASE 3: FINAL SUBMISSION, COGNITIVE SCORING & CATBOOST INFERENCE"},
        {"type": "call", "y": 11.3, "from": 1.2, "to": 4.0, "text": "14. POST /api/assessment/submit (Trigger AI Glassmorphism Loading Overlay)", "color": "#0284c7"},
        {"type": "call", "y": 10.5, "from": 4.0, "to": 9.6, "text": "15. BEGIN TRANSACTION -> SELECT student_answers WHERE assessment_id = ?", "color": "#d97706"},
        {"type": "call", "y": 9.7, "from": 4.0, "to": 12.4, "text": "16. Compute 16 Cognitive Abilities & 8 Interests -> INSERT INTO assessment_scores", "color": "#db2777"},
        {"type": "call", "y": 8.9, "from": 12.4, "to": 6.8, "text": "17. Fetch Student Demographics & Academic Subject Marks", "color": "#059669"},
        {"type": "call", "y": 8.1, "from": 12.4, "to": 12.4, "text": "18. CatBoost Model: Predict Top-5 Matches (Hit@5 = 98.55%, NDCG@5 = 0.9475)", "color": "#db2777", "self": True},
        {"type": "call", "y": 7.3, "from": 12.4, "to": 15.0, "text": "19. INSERT INTO career_recommendations (Top 5 Careers with strengths & gaps)", "color": "#7c3aed"},
        {"type": "call", "y": 6.5, "from": 4.0, "to": 9.6, "text": "20. UPDATE assessment_sessions SET status='completed', completed_at=NOW() -> COMMIT", "color": "#d97706"},
        {"type": "return", "y": 5.8, "from": 4.0, "to": 1.2, "text": "21. 200 OK -> JSON { status: 'completed', redirect_url: '/assessment/results' }", "color": "#0284c7"},

        # PHASE 4: RESULTS & CAREER ROADMAP EXPLORATION
        {"type": "phase", "y": 5.0, "title": "PHASE 4: RESULTS VISUALIZATION & CAREER ROADMAP RETRIEVAL"},
        {"type": "call", "y": 4.1, "from": 1.2, "to": 15.0, "text": "22. GET /assessment/results (Query Top-5 Recs, Radar Charts, Career Pathways)", "color": "#7c3aed"},
        {"type": "call", "y": 3.3, "from": 4.0, "to": 15.0, "text": "23. SELECT careers JOIN career_skills JOIN career_education JOIN career_pathways", "color": "#7c3aed"},
        {"type": "return", "y": 2.5, "from": 15.0, "to": 1.2, "text": "24. Render Interactive Results Dashboard (Roadmaps, Degrees, Match Scores)", "color": "#0284c7"}
    ]

    for step in steps:
        if step["type"] == "phase":
            y = step["y"]
            # Phase Banner
            p_box = patches.FancyBboxPatch((0.5, y - 0.3), 15.2, 0.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                                          edgecolor='#e2e8f0', facecolor='#f1f5f9', zorder=2)
            ax.add_patch(p_box)
            ax.text(8.1, y, step["title"], ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1e293b', zorder=3)

        elif step["type"] == "call":
            y = step["y"]
            x_from = step["from"]
            x_to = step["to"]
            col = step["color"]
            dashed = step.get("dashed", False)
            ls = '--' if dashed else '-'

            if step.get("self", False):
                # Self loop arrow
                arc = patches.Arc((x_from + 0.5, y), 1.0, 0.4, angle=0, theta1=270, theta2=90, color=col, linewidth=1.5, zorder=3)
                ax.add_patch(arc)
                ax.annotate('', xy=(x_from, y - 0.2), xytext=(x_from + 0.1, y - 0.2),
                            arrowprops=dict(arrowstyle="->", color=col, lw=1.5), zorder=3)
                ax.text(x_from + 1.1, y, step["text"], ha='left', va='center', fontsize=7.2, fontweight='bold', color='#334155', zorder=4)
            else:
                ax.annotate('', xy=(x_to, y), xytext=(x_from, y),
                            arrowprops=dict(arrowstyle="->", color=col, lw=1.4, linestyle=ls), zorder=3)
                mid_x = (x_from + x_to) / 2.0
                # Small white text backdrop for clear legibility
                ax.text(mid_x, y + 0.18, step["text"], ha='center', va='bottom', fontsize=7.2, fontweight='semibold',
                        color='#0f172a', bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffffff', edgecolor='#e2e8f0', lw=0.5), zorder=4)

        elif step["type"] == "return":
            y = step["y"]
            x_from = step["from"]
            x_to = step["to"]
            col = step["color"]
            dashed = step.get("dashed", True)
            ls = '--' if dashed else '-'

            ax.annotate('', xy=(x_to, y), xytext=(x_from, y),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.3, linestyle=ls), zorder=3)
            mid_x = (x_from + x_to) / 2.0
            ax.text(mid_x, y + 0.18, step["text"], ha='center', va='bottom', fontsize=7.0, style='italic',
                    color='#334155', bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffffff', edgecolor='#e2e8f0', lw=0.5), zorder=4)

    plt.tight_layout()
    img_path = OUTPUT_DIR / "database_sequence_diagram.png"
    plt.savefig(str(img_path), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated Sequence Diagram at: {img_path}")
    return img_path

if __name__ == '__main__':
    generate_database_sequence_diagram()
