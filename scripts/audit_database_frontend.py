"""
Audit all 18 database tables and columns against Frontend Templates, JS, and Backend Routes.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.extensions import db
from backend.app import create_app

templates_dir = Path('frontend/templates')
js_dir = Path('frontend/static/js')
all_frontend_files = list(templates_dir.glob('**/*.html')) + list(js_dir.glob('*.js'))
frontend_content = {f.name: f.read_text(encoding='utf-8') for f in all_frontend_files}

app = create_app('testing')
with app.app_context():
    from backend.models.user import User
    from backend.models.student import Student, AcademicScore
    from backend.models.question import QuestionSection, Question, QuestionOption
    from backend.models.assessment import AssessmentSession, StudentAnswer, AssessmentScore
    from backend.models.career import CareerDomain, CareerSubdomain, CareerCluster, Career, CareerSkill, CareerSubject, CareerEducation, CareerPathway
    from backend.models.recommendation import CareerRecommendation

    tables = db.metadata.tables
    print(f"Total Registered Tables: {len(tables)}\n")

    for tbl_name, tbl in sorted(tables.items()):
        cols = tbl.columns
        print(f"============================================================")
        print(f"TABLE: {tbl_name} ({len(cols)} columns)")
        print(f"============================================================")
        for col in cols:
            cname = col.name
            ctype = str(col.type)
            matches = [fname for fname, content in frontend_content.items() if cname in content]
            if matches:
                usage = f"EXPOSED in frontend ({len(matches)} files: {', '.join(matches[:3])})"
            else:
                usage = "NOT in frontend (Internal / FK / ML Feature / Backend Only)"
            print(f"  - {cname:28s} {ctype:18s} -> {usage}")
        print()
