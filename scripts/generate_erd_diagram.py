"""
Generate High-Resolution Entity Relationship & Transaction Flow Architecture Diagram.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "database"

def generate_database_erd_diagram():
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Title
    ax.text(8.0, 11.5, "DATABASE RELATIONAL SCHEMA & DATA FLOW ARCHITECTURE", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#0f172a')
    ax.text(8.0, 11.0, "18 Normalized Tables Segregated Across 6 Core Modules with Machine Learning Feature Extraction", 
            ha='center', va='center', fontsize=9.5, color='#64748b', style='italic')

    # Module Clusters Boxes
    modules = [
        # (x, y, w, h, title, color, tables)
        (0.6, 6.2, 4.4, 4.2, "MODULE A: USER & STUDENT AUTH", "#0284c7", [
            ("users", "7 Cols", "PK: id | username, email, pwd, role"),
            ("students", "13 Cols", "PK: id | FK: user_id | age, class, board, stream"),
            ("academic_scores", "21 Cols", "PK: id | FK: student_id | 17 subjects + overall%")
        ]),
        (5.8, 6.2, 4.4, 4.2, "MODULE B: ADAPTIVE QUESTION ENGINE", "#d97706", [
            ("question_sections", "5 Cols", "PK: id | name, description, is_active"),
            ("questions", "15 Cols", "PK: id | FK: section_id | class_min/max, difficulty"),
            ("question_options", "7 Cols", "PK: id | FK: question_id | text, score, is_correct")
        ]),
        (11.0, 6.2, 4.4, 4.2, "MODULE C: ASSESSMENT SESSIONS", "#059669", [
            ("assessment_sessions", "9 Cols", "PK: id | FK: student_id | status, completion%"),
            ("student_answers", "9 Cols", "PK: id | FK: session_id, question_id | options"),
            ("assessment_scores", "25 Cols", "PK: id | FK: session_id | 16 Aptitudes, 8 Interests")
        ]),
        (0.6, 0.8, 4.4, 4.8, "MODULE D: CAREER TAXONOMY", "#7c3aed", [
            ("career_domains", "6 Cols", "PK: id | 33 Industry Domains"),
            ("career_subdomains", "4 Cols", "PK: id | FK: domain_id | 389 Subdomains"),
            ("career_clusters", "4 Cols", "PK: id | FK: subdomain_id | 466 Clusters"),
            ("careers", "16 Cols", "PK: id | 2,259 Master Occupations")
        ]),
        (5.8, 0.8, 4.4, 4.8, "MODULE E: CAREER KNOWLEDGE GRAPH", "#db2777", [
            ("career_skills", "5 Cols", "PK: id | FK: career_id | skill, weight"),
            ("career_subjects", "5 Cols", "PK: id | FK: career_id | subject, weight"),
            ("career_education", "6 Cols", "PK: id | FK: career_id | degree milestones"),
            ("career_pathways", "5 Cols", "PK: id | FK: career_id | progression ladder")
        ]),
        (11.0, 0.8, 4.4, 4.8, "MODULE F: CATBOOST ML INFERENCE", "#4f46e5", [
            ("CatBoost Classifier", "V9.5", "86.22% Acc | 98.55% Hit@5 | 0.9475 NDCG"),
            ("career_recommendations", "9 Cols", "PK: id | FK: session_id, career_id | Top 5"),
            ("Results Dashboard", "UI View", "Radar Charts, RIASEC, Strengths, Skill Gaps")
        ])
    ]

    for m in modules:
        mx, my, mw, mh, mtitle, mcol, mtables = m
        # Outer card
        card = patches.FancyBboxPatch((mx, my), mw, mh, boxstyle="round,pad=0.1,rounding_size=0.2",
                                      edgecolor=mcol, facecolor='#f8fafc', linewidth=1.5, zorder=2)
        ax.add_patch(card)
        # Header banner
        head = patches.FancyBboxPatch((mx, my + mh - 0.7), mw, 0.7, boxstyle="round,pad=0.05,rounding_size=0.1",
                                      edgecolor=mcol, facecolor=mcol, zorder=3)
        ax.add_patch(head)
        ax.text(mx + mw/2, my + mh - 0.35, mtitle, ha='center', va='center', fontsize=8.0, fontweight='bold', color='#ffffff', zorder=4)

        # Render tables inside
        ty = my + mh - 1.1
        for tname, tmeta, tdesc in mtables:
            t_box = patches.FancyBboxPatch((mx + 0.2, ty - 0.7), mw - 0.4, 0.75, boxstyle="round,pad=0.05,rounding_size=0.08",
                                           edgecolor='#cbd5e1', facecolor='#ffffff', linewidth=0.8, zorder=3)
            ax.add_patch(t_box)
            ax.text(mx + 0.35, ty - 0.18, tname, ha='left', va='center', fontsize=8.0, fontweight='bold', color='#0f172a', zorder=4)
            ax.text(mx + mw - 0.35, ty - 0.18, tmeta, ha='right', va='center', fontsize=7.0, fontweight='bold', color=mcol, zorder=4)
            ax.text(mx + 0.35, ty - 0.48, tdesc, ha='left', va='center', fontsize=6.5, color='#64748b', zorder=4)
            ty -= 0.95

    # Draw Inter-Module Flow Connectors
    # A -> C (Student creates session)
    ax.annotate('', xy=(11.0, 8.5), xytext=(5.0, 8.5),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2, linestyle="-"), zorder=5)
    ax.text(8.0, 8.7, "Student & Academic Scores -> Starts Assessment", ha='center', va='bottom', fontsize=7.0, fontweight='bold', color='#0284c7')

    # B -> C (Questions loaded into session)
    ax.annotate('', xy=(11.0, 7.2), xytext=(10.2, 7.2),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=2, linestyle="-"), zorder=5)
    ax.text(10.6, 7.4, "Adaptive Questions", ha='center', va='bottom', fontsize=6.8, fontweight='bold', color='#d97706')

    # C -> F (Assessment scores feed ML)
    ax.annotate('', xy=(13.2, 5.6), xytext=(13.2, 6.2),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2, linestyle="-"), zorder=5)
    ax.text(13.5, 5.9, "16 Aptitudes + 8 Interests", ha='left', va='center', fontsize=7.0, fontweight='bold', color='#059669')

    # D -> E (Taxonomy links to knowledge graph)
    ax.annotate('', xy=(5.8, 3.2), xytext=(5.0, 3.2),
                arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=2, linestyle="-"), zorder=5)
    ax.text(5.4, 3.4, "1:N Relations", ha='center', va='bottom', fontsize=7.0, fontweight='bold', color='#7c3aed')

    # E -> F (Knowledge & taxonomy feeds ML vector and recommendation justifications)
    ax.annotate('', xy=(11.0, 3.2), xytext=(10.2, 3.2),
                arrowprops=dict(arrowstyle="->", color="#db2777", lw=2, linestyle="-"), zorder=5)
    ax.text(10.6, 3.4, "Skills, Subjects, Pathways", ha='center', va='bottom', fontsize=6.8, fontweight='bold', color='#db2777')

    plt.tight_layout()
    img_path = OUTPUT_DIR / "database_erd_flow.png"
    plt.savefig(str(img_path), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated ERD Flow Diagram at: {img_path}")
    return img_path

if __name__ == '__main__':
    generate_database_erd_diagram()
