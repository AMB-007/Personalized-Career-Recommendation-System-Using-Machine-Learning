"""
Diagram generator for PathFinder Academic Project Report.
Creates all architecture, DFD, UML, ER diagrams and saves to docs/report_figures/
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR  = os.path.join(BASE_DIR, "docs", "report_figures")
ML_FIGS  = os.path.join(BASE_DIR, "ml", "reports", "model_figures")
os.makedirs(OUT_DIR, exist_ok=True)

NAVY   = '#1B2631'
BLUE   = '#1A5276'
TEAL   = '#0E6655'
GREEN  = '#1E8449'
ORANGE = '#D35400'
PURPLE = '#6C3483'
GRAY   = '#566573'
LGRAY  = '#AEB6BF'
WHITE  = '#FFFFFF'
LBLUE  = '#D6EAF8'
LTEAL  = '#D1F2EB'
LORANGE= '#FDEBD0'
LPURP  = '#E8DAEF'


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {name}")


def box(ax, x, y, w, h, label, sublabel='', fc='#D6EAF8', ec='#1A5276', fs=9, sfs=7):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle="round,pad=0.02", linewidth=1.2,
                           edgecolor=ec, facecolor=fc)
    ax.add_patch(rect)
    ax.text(x, y + (0.015 if sublabel else 0), label, ha='center', va='center',
            fontsize=fs, fontweight='bold', color=NAVY, wrap=True)
    if sublabel:
        ax.text(x, y - 0.035, sublabel, ha='center', va='center',
                fontsize=sfs, color=GRAY)


def arrow(ax, x1, y1, x2, y2, color=BLUE, lw=1.2, style='->', label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.01, my, label, fontsize=6.5, color=color, va='center')


# ─────────────────────────────────────────────────────────────────
# 01 - System Architecture
# ─────────────────────────────────────────────────────────────────
def gen_system_architecture():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    ax.text(0.5, 0.96, 'PathFinder – 4-Tier System Architecture', ha='center', va='top',
            fontsize=13, fontweight='bold', color=NAVY)

    # Tier labels
    tier_info = [
        (0.02, 0.78, 'TIER 1\nClient\nBrowser', '#F9F0FF', PURPLE),
        (0.02, 0.58, 'TIER 2\nFlask Web\nLayer', '#EBF5FB', BLUE),
        (0.02, 0.36, 'TIER 3\nDomain\nServices', '#E9F7EF', TEAL),
        (0.02, 0.13, 'TIER 4\nPersistence\nLayer', '#FEF9E7', ORANGE),
    ]
    for tx, ty, label, fc, ec in tier_info:
        rect = FancyBboxPatch((tx, ty-0.10), 0.09, 0.20, boxstyle="round,pad=0.01",
                               facecolor=fc, edgecolor=ec, linewidth=1.5, alpha=0.7)
        ax.add_patch(rect)
        ax.text(tx+0.045, ty, label, ha='center', va='center', fontsize=7,
                fontweight='bold', color=ec)

    # Tier 1 – Client
    clients = [('Student\nBrowser', 0.25), ('Admin\nBrowser', 0.45), ('Mobile\nBrowser', 0.65)]
    for label, cx in clients:
        box(ax, cx, 0.78, 0.14, 0.14, label, fc='#E8DAEF', ec=PURPLE, fs=8)

    # Tier 2 – Flask
    blueprints = [
        ('auth\nBlueprint', 0.20), ('student\nBlueprint', 0.35),
        ('assessment\nBlueprint', 0.50), ('career\nBlueprint', 0.65),
        ('admin\nBlueprint', 0.80)
    ]
    for label, cx in blueprints:
        box(ax, cx, 0.58, 0.12, 0.12, label, fc=LBLUE, ec=BLUE, fs=7)

    # Tier 3 – Services
    services = [
        ('Auth\nService', 0.18), ('Assessment\nEngine', 0.32),
        ('ML\nInference', 0.46), ('Career\nService', 0.60),
        ('Admin\nAnalytics', 0.74), ('Notification\nService', 0.88)
    ]
    for label, cx in services:
        box(ax, cx, 0.36, 0.12, 0.12, label, fc=LTEAL, ec=TEAL, fs=7)

    # ML sub-box
    ml_rect = FancyBboxPatch((0.395, 0.27), 0.13, 0.11, boxstyle="round,pad=0.01",
                              facecolor='#FDFEFE', edgecolor=ORANGE, linewidth=1.2, linestyle='--')
    ax.add_patch(ml_rect)
    ax.text(0.46, 0.325, 'XGBoost\nChampion V8', ha='center', va='center',
            fontsize=6.5, color=ORANGE, fontweight='bold')

    # Tier 4 – Persistence
    stores = [
        ('MySQL\ncareer_recommendation_db\n14 Tables', 0.26, '#FEF9E7', ORANGE),
        ('Model\nArtifacts\nJoblib Files', 0.50, '#FDEDEC', '#C0392B'),
        ('Session\nStore\nFlask Sessions', 0.74, '#EBF5FB', BLUE),
    ]
    for label, cx, fc, ec in stores:
        box(ax, cx, 0.13, 0.20, 0.14, label, fc=fc, ec=ec, fs=7)

    # Arrows tier 1->2
    for cx in [0.25, 0.45, 0.65]:
        bx = 0.20 + [0.25,0.45,0.65].index(cx) * 0.15
        arrow(ax, cx, 0.71, bx+0.08, 0.64, PURPLE, 1.0)

    # Arrows tier 2->3
    for i, (_, cx) in enumerate(blueprints):
        sx = services[min(i, len(services)-1)][1]
        arrow(ax, cx, 0.52, sx, 0.42, BLUE, 1.0)

    # Arrows tier 3->4
    arrow(ax, 0.32, 0.30, 0.26, 0.21, TEAL)
    arrow(ax, 0.46, 0.30, 0.50, 0.21, ORANGE)
    arrow(ax, 0.60, 0.30, 0.74, 0.21, BLUE)

    save(fig, '01_system_architecture.png')


# ─────────────────────────────────────────────────────────────────
# 02 - DFD Level 0 (Context Diagram)
# ─────────────────────────────────────────────────────────────────
def gen_dfd0():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(0.5, 0.96, 'DFD Level 0 – Context Diagram', ha='center', va='top',
            fontsize=13, fontweight='bold', color=NAVY)

    # System bubble
    circle = plt.Circle((0.5, 0.5), 0.18, color=LBLUE, ec=BLUE, lw=2.5, zorder=3)
    ax.add_patch(circle)
    ax.text(0.5, 0.52, 'PathFinder', ha='center', va='center',
            fontsize=11, fontweight='bold', color=NAVY, zorder=4)
    ax.text(0.5, 0.46, 'System', ha='center', va='center',
            fontsize=9, color=BLUE, zorder=4)

    # External entities
    entities = [
        ('Student\n(Class 7-12)', 0.08, 0.50, '#E8DAEF', PURPLE),
        ('Admin /\nCounsellor',   0.92, 0.50, '#FDEBD0', ORANGE),
        ('MySQL\nDatabase',       0.50, 0.06, '#D5F5E3', GREEN),
        ('ML Model\nArtifacts',   0.50, 0.92, '#FDEDEC', '#C0392B'),
    ]
    for label, ex, ey, fc, ec in entities:
        box(ax, ex, ey, 0.14, 0.12, label, fc=fc, ec=ec, fs=9)

    # Data flows
    flows = [
        (0.22, 0.50, 0.32, 0.50, 'Assessment Answers\nCareer Queries', PURPLE, 0.52),
        (0.68, 0.50, 0.78, 0.50, 'System Reports\nAnalytics Dashboards', ORANGE, 0.52),
        (0.50, 0.32, 0.50, 0.18, 'Read/Write\nRelational Data', GREEN, 0.50),
        (0.50, 0.68, 0.50, 0.80, 'Model Load\nInference Requests', '#C0392B', 0.50),
    ]
    for x1, y1, x2, y2, lbl, col, lx in flows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='<->', color=col, lw=1.5))
        ax.text(lx, (y1+y2)/2 + 0.03, lbl, ha='center', va='bottom',
                fontsize=7.5, color=col)

    # Return flows (labels)
    ax.text(0.26, 0.44, 'Top-10 Career\nRecommendations', ha='center', va='top',
            fontsize=7.5, color=PURPLE)
    ax.text(0.74, 0.44, 'Management\nCRUD Operations', ha='center', va='top',
            fontsize=7.5, color=ORANGE)

    save(fig, '02_dfd_level_0.png')


# ─────────────────────────────────────────────────────────────────
# 03 - DFD Level 1
# ─────────────────────────────────────────────────────────────────
def gen_dfd1():
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(0.5, 0.97, 'DFD Level 1 – Functional Decomposition (6 Subsystems)', ha='center', va='top',
            fontsize=12, fontweight='bold', color=NAVY)

    # Processes (ovals)
    processes = [
        (0.20, 0.75, '1.0\nAuthentication\n& Authorization'),
        (0.50, 0.75, '2.0\nPsychometric\nAssessment Engine'),
        (0.80, 0.75, '3.0\nScore\nCalculation'),
        (0.20, 0.35, '4.0\nML Inference\n& Ranking'),
        (0.50, 0.35, '5.0\nCareer\nRecommendation'),
        (0.80, 0.35, '6.0\nAdmin\nManagement'),
    ]
    colors_p = [LBLUE, LTEAL, LORANGE, '#FDEDEC', LPURP, '#FDFEFE']
    edge_p   = [BLUE, TEAL, ORANGE, '#C0392B', PURPLE, GRAY]
    for i, (px, py, label) in enumerate(processes):
        ell = mpatches.Ellipse((px, py), 0.22, 0.14, color=colors_p[i],
                                ec=edge_p[i], lw=1.5)
        ax.add_patch(ell)
        ax.text(px, py, label, ha='center', va='center',
                fontsize=8, fontweight='bold', color=NAVY)

    # Data stores (open rectangles)
    stores = [
        (0.15, 0.55, 'DS1: users\n& students'),
        (0.50, 0.55, 'DS2: questions\n& answers'),
        (0.85, 0.55, 'DS3: assessment\n_scores'),
        (0.15, 0.15, 'DS4: careers\n& taxonomy'),
        (0.85, 0.15, 'DS5: career_\nrecommendations'),
    ]
    for sx, sy, label in stores:
        rect = plt.Rectangle((sx-0.09, sy-0.04), 0.18, 0.08,
                              facecolor='#F8F9FA', edgecolor=GRAY, lw=1.2)
        ax.add_patch(rect)
        # Open left side
        rect2 = plt.Rectangle((sx-0.09, sy-0.04), 0.01, 0.08,
                               facecolor='white', edgecolor='white')
        ax.add_patch(rect2)
        ax.text(sx, sy, label, ha='center', va='center', fontsize=7.5, color=NAVY)

    # External entities
    box(ax, 0.05, 0.75, 0.08, 0.10, 'Student', fc='#E8DAEF', ec=PURPLE, fs=8)
    box(ax, 0.95, 0.75, 0.08, 0.10, 'Admin', fc='#FDEBD0', ec=ORANGE, fs=8)

    # Flow arrows (simplified)
    flows = [
        (0.09, 0.75, 0.09, 0.75),  # student to auth
    ]
    ax.annotate('', xy=(0.09, 0.75), xytext=(0.05, 0.75),
                arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1.2))
    ax.annotate('', xy=(0.39, 0.75), xytext=(0.31, 0.75),
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.2))
    ax.annotate('', xy=(0.69, 0.75), xytext=(0.61, 0.75),
                arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.2))
    ax.annotate('', xy=(0.50, 0.61), xytext=(0.50, 0.68),
                arrowprops=dict(arrowstyle='<->', color=GRAY, lw=1.2))
    ax.annotate('', xy=(0.80, 0.61), xytext=(0.80, 0.68),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2))
    ax.annotate('', xy=(0.20, 0.42), xytext=(0.20, 0.55),
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.2))
    ax.annotate('', xy=(0.39, 0.35), xytext=(0.31, 0.35),
                arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1.2))
    ax.annotate('', xy=(0.85, 0.23), xytext=(0.71, 0.35),
                arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1.2))
    ax.annotate('', xy=(0.91, 0.75), xytext=(0.91, 0.75),
                arrowprops=dict(arrowstyle='<-', color=ORANGE, lw=1.2))
    ax.annotate('', xy=(0.91, 0.35), xytext=(0.91, 0.35),
                arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=1.2))

    # Flow labels
    ax.text(0.07, 0.78, 'Login', fontsize=7, color=PURPLE)
    ax.text(0.35, 0.78, 'Answers', fontsize=7, color=BLUE)
    ax.text(0.63, 0.78, 'Scores', fontsize=7, color=TEAL)
    ax.text(0.34, 0.36, 'Top-K Careers', fontsize=7, color=PURPLE)

    DARK = NAVY
    save(fig, '03_dfd_level_1.png')


# ─────────────────────────────────────────────────────────────────
# 04 - DFD Level 2 (ML Inference)
# ─────────────────────────────────────────────────────────────────
def gen_dfd2():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(0.5, 0.97, 'DFD Level 2 – ML Inference & Assessment Scoring Subsystem', ha='center', va='top',
            fontsize=12, fontweight='bold', color=NAVY)

    steps = [
        (0.12, 0.60, '2.1\nLoad Student\nProfile & Marks',   LBLUE,  BLUE),
        (0.28, 0.60, '2.2\nCompute 22\nDimension Scores',    LTEAL,  TEAL),
        (0.45, 0.60, '2.3\nEngineer 11\nML Features',        LORANGE,ORANGE),
        (0.62, 0.60, '2.4\nBatch XGBoost\nInference\n(2259)',  '#FDEDEC','#C0392B'),
        (0.78, 0.60, '2.5\nCosine Synergy\nRe-Ranking',      LPURP,  PURPLE),
        (0.93, 0.60, '2.6\nStore Top-10\nResults',           '#E9F7EF',GREEN),
    ]
    w, h = 0.13, 0.18
    for px, py, label, fc, ec in steps:
        box(ax, px, py, w, h, label, fc=fc, ec=ec, fs=8)

    # Arrows between steps
    for i in range(len(steps)-1):
        x1 = steps[i][0] + w/2
        x2 = steps[i+1][0] - w/2
        y  = steps[i][1]
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.4))

    # Data stores below
    ds_items = [
        (0.20, 0.25, 'students\nacademic_scores\nassessment_sessions', LTEAL, TEAL),
        (0.50, 0.25, 'model.joblib\npreprocessor.joblib\nfeature_columns.json', '#FDEDEC', '#C0392B'),
        (0.80, 0.25, 'careers (2259)\ncareer_recommendations\n(Top-10 per test)', '#E9F7EF', GREEN),
    ]
    for dx, dy, label, fc, ec in ds_items:
        rect = FancyBboxPatch((dx-0.14, dy-0.10), 0.28, 0.20,
                               boxstyle="round,pad=0.01", facecolor=fc, edgecolor=ec, lw=1.2)
        ax.add_patch(rect)
        ax.text(dx, dy, label, ha='center', va='center', fontsize=7.5, color=NAVY)

    # Vertical arrows from process to datastores
    ax.annotate('', xy=(0.20, 0.35), xytext=(0.20, 0.51),
                arrowprops=dict(arrowstyle='<->', color=TEAL, lw=1.2))
    ax.annotate('', xy=(0.50, 0.35), xytext=(0.62, 0.51),
                arrowprops=dict(arrowstyle='<-', color='#C0392B', lw=1.2))
    ax.annotate('', xy=(0.80, 0.35), xytext=(0.93, 0.51),
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))

    ax.text(0.20, 0.43, 'Read Profile', ha='center', fontsize=7, color=TEAL)
    ax.text(0.56, 0.43, 'Load Model', ha='right', fontsize=7, color='#C0392B')
    ax.text(0.88, 0.43, 'Persist Results', ha='right', fontsize=7, color=GREEN)

    save(fig, '04_dfd_level_2.png')


# ─────────────────────────────────────────────────────────────────
# 05 - UML Use Case
# ─────────────────────────────────────────────────────────────────
def gen_uml_usecase():
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(0.5, 0.97, 'UML Use Case Diagram – PathFinder System', ha='center', va='top',
            fontsize=13, fontweight='bold', color=NAVY)

    # System boundary
    sys_rect = FancyBboxPatch((0.14, 0.05), 0.72, 0.88, boxstyle="round,pad=0.01",
                               facecolor='#F8FBFF', edgecolor=BLUE, lw=2.0)
    ax.add_patch(sys_rect)
    ax.text(0.50, 0.91, '<< PathFinder System Boundary >>', ha='center', va='center',
            fontsize=9, color=BLUE, style='italic')

    # Actors
    def actor(ax, x, y, label, color=NAVY):
        # Head
        circ = plt.Circle((x, y+0.055), 0.022, color='white', ec=color, lw=1.5)
        ax.add_patch(circ)
        # Body
        ax.plot([x, x], [y+0.033, y-0.03], color=color, lw=1.5)
        # Arms
        ax.plot([x-0.025, x+0.025], [y+0.015, y+0.015], color=color, lw=1.5)
        # Legs
        ax.plot([x, x-0.02], [y-0.03, y-0.06], color=color, lw=1.5)
        ax.plot([x, x+0.02], [y-0.03, y-0.06], color=color, lw=1.5)
        ax.text(x, y-0.075, label, ha='center', va='top', fontsize=8,
                fontweight='bold', color=color)

    actor(ax, 0.06, 0.60, 'Student\n(Class 7-12)', PURPLE)
    actor(ax, 0.94, 0.55, 'Admin /\nCounsellor', ORANGE)

    # Use cases (ellipses)
    uc_student = [
        (0.30, 0.82, 'Register & Login'),
        (0.30, 0.70, 'Complete Psychometric\nAssessment (19 dims)'),
        (0.30, 0.58, 'View Cognitive\nRadar Profile'),
        (0.30, 0.46, 'Get Top-10 Career\nRecommendations'),
        (0.30, 0.34, 'Explore Career\nRoadmap (5 Stages)'),
        (0.30, 0.22, 'Browse Career\nTaxonomy (2,259)'),
    ]
    uc_admin = [
        (0.65, 0.82, 'Manage Students\n& Users'),
        (0.65, 0.70, 'CRUD Questions\n& Options (413)'),
        (0.65, 0.58, 'Manage Careers\n& Taxonomy'),
        (0.65, 0.46, 'View System\nAnalytics'),
        (0.65, 0.34, 'Export Reports\n& Audit Logs'),
    ]

    def uc_ellipse(ax, x, y, label, color=BLUE):
        ell = mpatches.Ellipse((x, y), 0.25, 0.09, color='white', ec=color, lw=1.3)
        ax.add_patch(ell)
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5, color=NAVY)

    for x, y, label in uc_student:
        uc_ellipse(ax, x, y, label, BLUE)
        ax.plot([0.10, x-0.125], [0.60, y], color=PURPLE, lw=0.8, alpha=0.6)

    for x, y, label in uc_admin:
        uc_ellipse(ax, x, y, label, ORANGE)
        ax.plot([0.88, x+0.125], [0.55, y], color=ORANGE, lw=0.8, alpha=0.6)

    # Shared use case
    uc_ellipse(ax, 0.50, 0.12, 'View SHAP\nExplanations', TEAL)
    ax.plot([0.30, 0.375], [0.22, 0.12], color=TEAL, lw=0.8, linestyle='--')
    ax.plot([0.65, 0.625], [0.34, 0.12], color=TEAL, lw=0.8, linestyle='--')

    save(fig, '05_uml_use_case.png')


# ─────────────────────────────────────────────────────────────────
# 06 - UML Sequence Diagram
# ─────────────────────────────────────────────────────────────────
def gen_uml_sequence():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(0.5, 0.97, 'UML Sequence Diagram – Assessment Lifecycle to Top-K Recommendations',
            ha='center', va='top', fontsize=12, fontweight='bold', color=NAVY)

    # Lifelines
    participants = [
        (0.08, 'Student\nBrowser', PURPLE),
        (0.24, 'Flask\nRouter', BLUE),
        (0.40, 'Assessment\nService', TEAL),
        (0.56, 'Score\nCalculator', ORANGE),
        (0.72, 'ML\nInference', '#C0392B'),
        (0.88, 'MySQL\nDatabase', GREEN),
    ]
    top_y = 0.92
    bot_y = 0.04
    for lx, label, color in participants:
        box(ax, lx, top_y, 0.12, 0.06, label, fc='white', ec=color, fs=8)
        ax.plot([lx, lx], [top_y - 0.03, bot_y], color=color, lw=1.0,
                linestyle='--', alpha=0.6)

    # Messages (y positions from top to bottom)
    messages = [
        (0.88, 0.24, 0.56, '1. POST /auth/login', PURPLE, '->'),
        (0.84, 0.24, 0.40, '2. GET /assessment/start', BLUE, '->'),
        (0.80, 0.40, 0.88, '3. Load grade-filtered questions', TEAL, '->'),
        (0.76, 0.88, 0.40, '4. Return 140-163 questions', GREEN, '-->'),
        (0.72, 0.40, 0.08, '5. Render adaptive questionnaire', TEAL, '-->'),
        (0.68, 0.08, 0.24, '6. POST answer (AJAX autosave)', PURPLE, '->'),
        (0.64, 0.24, 0.40, '7. Validate & store answer', BLUE, '->'),
        (0.60, 0.40, 0.88, '8. INSERT student_answers', TEAL, '->'),
        (0.56, 0.08, 0.24, '9. POST /assessment/submit', PURPLE, '->'),
        (0.52, 0.24, 0.40, '10. Trigger score calculation', BLUE, '->'),
        (0.48, 0.40, 0.56, '11. Compute 22-dim scores', TEAL, '->'),
        (0.44, 0.56, 0.72, '12. Engineer 11 ML features', ORANGE, '->'),
        (0.40, 0.72, 0.88, '13. Batch XGBoost inference (2259)', '#C0392B', '->'),
        (0.36, 0.88, 0.72, '14. Return compatibility scores', GREEN, '-->'),
        (0.32, 0.72, 0.56, '15. Cosine re-rank Top-10', '#C0392B', '-->'),
        (0.28, 0.56, 0.40, '16. Return ranked career list', ORANGE, '-->'),
        (0.24, 0.40, 0.88, '17. INSERT career_recommendations', TEAL, '->'),
        (0.20, 0.40, 0.08, '18. Render results + SHAP charts', TEAL, '-->'),
        (0.14, 0.08, 0.08, '19. Display Radar + Top-10 Cards', PURPLE, ''),
    ]

    for y, x1, x2, label, color, style in messages:
        if style == '->':
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.2))
        elif style == '-->':
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.0,
                                        linestyle='dashed',
                                        connectionstyle='arc3'))
        direction = 'right' if x2 > x1 else 'left'
        mx = (x1 + x2) / 2
        ax.text(mx, y + 0.01, label, ha='center', va='bottom',
                fontsize=6.8, color=color)

    save(fig, '06_uml_sequence.png')


# ─────────────────────────────────────────────────────────────────
# 07 - Module Architecture
# ─────────────────────────────────────────────────────────────────
def gen_module_arch():
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(0.5, 0.97, 'PathFinder – Module Decomposition & Component Architecture',
            ha='center', va='top', fontsize=12, fontweight='bold', color=NAVY)

    # Backend modules
    modules = [
        (0.18, 0.78, 'backend/\nauth/', 'Registration\nLogin\nBcrypt Hash\nRBAC Roles', BLUE, LBLUE),
        (0.38, 0.78, 'backend/\nstudent/', 'Profile Manager\nAcademic Marks\nDashboard\nHistory', TEAL, LTEAL),
        (0.58, 0.78, 'backend/\nassessment/', 'Session Manager\nQ Delivery\nAutosave API\nScore Engine', ORANGE, LORANGE),
        (0.78, 0.78, 'backend/\ncareer/', 'Taxonomy Browser\nRoadmap Engine\nSearch & Filter\nRecommend API', PURPLE, LPURP),
        (0.18, 0.45, 'backend/\nadmin/', 'Student CRUD\nQ-Bank CRUD\nCareer CRUD\nAnalytics View', '#C0392B', '#FADBD8'),
        (0.38, 0.45, 'backend/\nml/', 'model_interface.py\nXGBoost Inference\nFeature Builder\nSHAP Explainer', '#C0392B', '#FADBD8'),
        (0.58, 0.45, 'backend/\nmodels/', '14 SQLAlchemy\nEntity Classes\nRelationships\nMigrations', GREEN, '#D5F5E3'),
        (0.78, 0.45, 'frontend/\ntemplates/', 'Jinja2 Templates\nChart.js Radars\nBootstrap 5 UI\nDark/Light Theme', GRAY, '#F2F3F4'),
    ]

    for mx, my, title, content, ec, fc in modules:
        outer = FancyBboxPatch((mx-0.10, my-0.14), 0.20, 0.28,
                                boxstyle="round,pad=0.01", facecolor=fc,
                                edgecolor=ec, lw=1.5)
        ax.add_patch(outer)
        ax.text(mx, my+0.09, title, ha='center', va='center',
                fontsize=8, fontweight='bold', color=NAVY)
        ax.plot([mx-0.10, mx+0.10], [my+0.04, my+0.04], color=ec, lw=0.8, alpha=0.6)
        for j, line in enumerate(content.split('\n')):
            ax.text(mx, my - 0.01 - j*0.032, '+ ' + line, ha='center', va='top',
                    fontsize=7, color=GRAY)

    # Database layer
    db_rect = FancyBboxPatch((0.08, 0.06), 0.84, 0.18,
                              boxstyle="round,pad=0.01",
                              facecolor='#FEF9E7', edgecolor=ORANGE, lw=2.0)
    ax.add_patch(db_rect)
    ax.text(0.50, 0.22, 'MySQL Database Layer – career_recommendation_db', ha='center', va='center',
            fontsize=9, fontweight='bold', color=NAVY)

    db_tables = ['users', 'students', 'academic_scores', 'questions (413)',
                 'question_options (1805)', 'assessment_sessions', 'student_answers',
                 'assessment_scores', 'careers (2259)', 'career_recommendations']
    ax.text(0.50, 0.13, '  |  '.join(db_tables), ha='center', va='center',
            fontsize=6.8, color=GRAY)

    # ML Artifacts box
    ml_box = FancyBboxPatch((0.35, 0.24), 0.30, 0.10,
                             boxstyle="round,pad=0.01",
                             facecolor='#FDEDEC', edgecolor='#C0392B', lw=1.5, linestyle='--')
    ax.add_patch(ml_box)
    ax.text(0.50, 0.29, 'ML Artifacts: model.joblib | preprocessor.joblib | feature_columns.json | model_config.json',
            ha='center', va='center', fontsize=7, color='#C0392B')

    # Arrows modules -> DB
    for mx in [0.18, 0.38, 0.58, 0.78]:
        ax.annotate('', xy=(mx, 0.24), xytext=(mx, 0.31),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=0.8))
    ax.annotate('', xy=(0.38, 0.34), xytext=(0.38, 0.31),
                arrowprops=dict(arrowstyle='<->', color='#C0392B', lw=1.0))

    save(fig, '07_module_architecture.png')


# ─────────────────────────────────────────────────────────────────
# 08 - ER Diagram
# ─────────────────────────────────────────────────────────────────
def gen_er_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.text(0.5, 0.97, 'Entity-Relationship (ER) Schema – 14 Relational Tables',
            ha='center', va='top', fontsize=13, fontweight='bold', color=NAVY)

    # Table boxes: (cx, cy, name, fields, color)
    tables = [
        (0.12, 0.80, 'users', ['id PK', 'username', 'email', 'password_hash', 'role', 'created_at'],
         BLUE, LBLUE),
        (0.38, 0.80, 'students', ['id PK', 'user_id FK', 'student_code', 'first_name', 'class_level', 'stream'],
         TEAL, LTEAL),
        (0.65, 0.80, 'academic_scores', ['id PK', 'student_id FK', '17 subject marks', 'overall_%'],
         ORANGE, LORANGE),
        (0.88, 0.80, 'assessment_sessions', ['id PK', 'student_id FK', 'status', 'started_at', 'completion_%'],
         PURPLE, LPURP),
        (0.12, 0.50, 'question_sections', ['id PK', 'name', 'description', 'display_order'],
         GRAY, '#F2F3F4'),
        (0.35, 0.50, 'questions', ['id PK', 'section_id FK', 'question_text', 'class_min/max', 'difficulty'],
         BLUE, LBLUE),
        (0.60, 0.50, 'question_options', ['id PK', 'question_id FK', 'option_text', 'score', 'is_correct'],
         TEAL, LTEAL),
        (0.85, 0.50, 'student_answers', ['id PK', 'assessment_id FK', 'question_id FK', 'selected_option_id'],
         ORANGE, LORANGE),
        (0.12, 0.20, 'career_domains', ['id PK', 'name', 'description', 'icon'],
         PURPLE, LPURP),
        (0.35, 0.20, 'career_subdomains', ['id PK', 'domain_id FK', 'name', 'description'],
         BLUE, LBLUE),
        (0.58, 0.20, 'career_clusters', ['id PK', 'subdomain_id FK', 'name', 'description'],
         TEAL, LTEAL),
        (0.80, 0.20, 'careers', ['id PK', 'cluster_id FK', 'career_code', 'name', 'min_education'],
         ORANGE, LORANGE),
        (0.38, 0.07, 'assessment_scores', ['id PK', 'assessment_id FK (1:1)', '22 dimension scores'],
         '#C0392B', '#FADBD8'),
        (0.70, 0.07, 'career_recommendations', ['id PK', 'assessment_id FK', 'career_id FK', 'rank', 'score'],
         PURPLE, LPURP),
    ]

    bw, bh = 0.17, 0.12
    for cx, cy, name, fields, ec, fc in tables:
        # Header
        header = FancyBboxPatch((cx-bw/2, cy+bh/2-0.025), bw, 0.028,
                                 boxstyle="round,pad=0.005", facecolor=ec, edgecolor=ec, lw=1.0)
        ax.add_patch(header)
        # Body
        body = FancyBboxPatch((cx-bw/2, cy-bh/2), bw, bh,
                               boxstyle="round,pad=0.005", facecolor=fc, edgecolor=ec, lw=1.0)
        ax.add_patch(body)
        ax.text(cx, cy+bh/2-0.011, name, ha='center', va='center',
                fontsize=7.5, fontweight='bold', color='white')
        for j, field in enumerate(fields[:5]):
            ax.text(cx, cy+bh/2-0.05-j*0.018, field, ha='center', va='top',
                    fontsize=6, color=NAVY)
        if len(fields) > 5:
            ax.text(cx, cy-bh/2+0.008, '...', ha='center', va='bottom',
                    fontsize=6, color=GRAY)

    # FK Relationships (lines)
    rels = [
        (0.12, 0.80, 0.38, 0.80, '1:1', BLUE),     # users -> students
        (0.38, 0.80, 0.65, 0.80, '1:1', TEAL),     # students -> academic_scores
        (0.38, 0.80, 0.88, 0.80, '1:N', PURPLE),   # students -> assessment_sessions
        (0.12, 0.50, 0.35, 0.50, '1:N', GRAY),     # sections -> questions
        (0.35, 0.50, 0.60, 0.50, '1:N', BLUE),     # questions -> options
        (0.88, 0.80, 0.85, 0.50, '1:N', ORANGE),   # sessions -> answers
        (0.12, 0.20, 0.35, 0.20, '1:N', PURPLE),   # domains -> subdomains
        (0.35, 0.20, 0.58, 0.20, '1:N', BLUE),     # subdomains -> clusters
        (0.58, 0.20, 0.80, 0.20, '1:N', TEAL),     # clusters -> careers
        (0.88, 0.50, 0.70, 0.07, '1:N', PURPLE),   # sessions -> recommendations
        (0.80, 0.20, 0.70, 0.07, 'N:1', ORANGE),   # careers -> recommendations
        (0.88, 0.80, 0.38, 0.07, '1:1', '#C0392B'),# sessions -> scores
    ]
    for x1, y1, x2, y2, card, color in rels:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=0.9, alpha=0.7))
        ax.text((x1+x2)/2, (y1+y2)/2+0.01, card, ha='center', va='bottom',
                fontsize=6.5, color=color, alpha=0.8)

    save(fig, '08_er_diagram.png')


# ─────────────────────────────────────────────────────────────────
# Also create ML overview figure (dataset table view)
# ─────────────────────────────────────────────────────────────────
def gen_ml_overview():
    """Summary table figure of dataset and features for Chapter 4"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('white')
    fig.suptitle('ML Training – Dataset Structure & Feature Schema', fontsize=12,
                 fontweight='bold', color=NAVY)

    ax1 = axes[0]
    ax1.axis('off')
    ax1.set_title('Dataset Statistics', fontsize=10, fontweight='bold', color=TEAL, pad=10)
    data1 = [
        ['Metric', 'Value'],
        ['Total Evaluations', '397,980 rows'],
        ['Student Profiles', '33,000 unique'],
        ['Career Profiles', '1,206 unique'],
        ['Compatible (Class 1)', '287,398 (72.21%)'],
        ['Incompatible (Class 0)', '110,582 (27.79%)'],
        ['Mean Compat. Score', '73.68% (Std: 6.28%)'],
        ['Grade Levels', 'Classes 7–12'],
        ['Train / Val / Test', '238,788 / 79,596 / 79,596'],
        ['Group CV', '5-Fold StratGroupKFold'],
        ['Student Leakage', 'ZERO (grouped by ID)'],
    ]
    t1 = ax1.table(cellText=data1[1:], colLabels=data1[0],
                   cellLoc='center', loc='center',
                   colWidths=[0.55, 0.45])
    t1.auto_set_font_size(False)
    t1.set_fontsize(8.5)
    for (r, c), cell in t1.get_celld().items():
        if r == 0:
            cell.set_facecolor(NAVY)
            cell.set_text_props(color='white', fontweight='bold')
        elif r % 2 == 0:
            cell.set_facecolor('#F0F8FF')
        cell.set_edgecolor('#E0E0E0')
        cell.set_height(0.072)
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)

    ax2 = axes[1]
    ax2.axis('off')
    ax2.set_title('11-Feature ML Schema Contract', fontsize=10, fontweight='bold', color=TEAL, pad=10)
    data2 = [
        ['Feature', 'Type', 'Role'],
        ['composite_alignment_index', 'Numeric', 'Primary composite metric'],
        ['ability_match_component', 'Numeric', 'Aptitude alignment score'],
        ['interest_match_component', 'Numeric', 'Interest dimension alignment'],
        ['academic_match_component', 'Numeric', 'Subject marks alignment'],
        ['learning_match_component', 'Numeric', 'Cognitive adaptability'],
        ['ability_interest_synergy', 'Numeric', 'Interaction term (ability x interest)'],
        ['ability_interest_gap', 'Numeric', 'Dissonance measure'],
        ['harmonic_core_match', 'Numeric', 'Harmonic mean of core 3'],
        ['min_core_match / max', 'Numeric', 'Bounding range features'],
        ['career_domain / cluster', 'Categorical', 'Taxonomy context (OrdinalEnc)'],
        ['stream / age / class', 'Mixed', 'Demographic context (<0.003 SHAP)'],
    ]
    t2 = ax2.table(cellText=data2[1:], colLabels=data2[0],
                   cellLoc='center', loc='center',
                   colWidths=[0.44, 0.20, 0.36])
    t2.auto_set_font_size(False)
    t2.set_fontsize(8)
    for (r, c), cell in t2.get_celld().items():
        if r == 0:
            cell.set_facecolor(TEAL)
            cell.set_text_props(color='white', fontweight='bold')
        elif r % 2 == 0:
            cell.set_facecolor('#F0FFF4')
        cell.set_edgecolor('#E0E0E0')
        cell.set_height(0.072)
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    os.makedirs(ML_FIGS, exist_ok=True)
    path = os.path.join(ML_FIGS, "00_dataset_tables_overview.png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: 00_dataset_tables_overview.png (ml/figures/)")


if __name__ == "__main__":
    print("Generating PathFinder Academic Report Diagrams...")
    print(f"Output directory: {OUT_DIR}")

    gen_system_architecture()
    gen_dfd0()
    gen_dfd1()
    gen_dfd2()
    gen_uml_usecase()
    gen_uml_sequence()
    gen_module_arch()
    gen_er_diagram()
    gen_ml_overview()

    print(f"\nAll diagrams generated in: {OUT_DIR}")
    print("Files created:")
    for f in sorted(os.listdir(OUT_DIR)):
        sz = os.path.getsize(os.path.join(OUT_DIR, f))
        print(f"  {f}  ({sz//1024} KB)")
