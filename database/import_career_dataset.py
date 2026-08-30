"""
Career Knowledge Dataset Import Pipeline.
Imports, normalizes, and maps Career_Knowledge_Requirements_Raw.csv into MySQL Server.
Preserves relational foreign-key integrity across domains, subdomains, clusters,
careers, skills, subjects, education pathways, and career progression stages.
Idempotent and safe to run repeatedly.
"""

import os
import sys
import csv
import re
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
import mysql.connector

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv(BASE_DIR / '.env')

# Domain icon mapping for rich UI presentation
DOMAIN_ICONS = {
    'Technology': 'bi-cpu',
    'Information Technology': 'bi-cpu',
    'Healthcare': 'bi-heart-pulse',
    'Medicine': 'bi-heart-pulse',
    'Engineering': 'bi-gear-wide-connected',
    'Pure Science': 'bi-radioactive',
    'Research': 'bi-search',
    'Business': 'bi-briefcase',
    'Finance': 'bi-graph-up-arrow',
    'Law': 'bi-shield-check',
    'Arts': 'bi-palette',
    'Design': 'bi-brush',
    'Media': 'bi-camera-reels',
    'Government': 'bi-building',
    'Agriculture': 'bi-tree',
    'Environment': 'bi-globe',
    'Sports': 'bi-trophy',
    'Hospitality': 'bi-cup-hot',
    'Aviation': 'bi-airplane',
    'Manufacturing': 'bi-tools',
    'Construction': 'bi-cone-striped',
    'Skilled Trades': 'bi-hammer',
    'Transportation': 'bi-truck',
    'Psychology and Social Sciences': 'bi-people',
    'Psychology And Social Sciences': 'bi-people',
    'Education': 'bi-mortarboard',
    'Biotechnology': 'bi-virus',
    'Pharmaceuticals': 'bi-capsule',
    'Defence and Security': 'bi-shield',
    'Defence And Security': 'bi-shield',
    'Fashion': 'bi-handbag',
    'Food': 'bi-egg-fried',
    'Real Estate': 'bi-house',
    'Emerging Careers': 'bi-stars',
    'Interdisciplinary': 'bi-diagram-3'
}

# Domain acronyms for deterministic code generation
DOMAIN_CODES = {
    'Technology': 'TECH',
    'Information Technology': 'IT',
    'Healthcare': 'HLTH',
    'Medicine': 'MED',
    'Engineering': 'ENG',
    'Pure Science': 'SCI',
    'Research': 'RES',
    'Business': 'BUS',
    'Finance': 'FIN',
    'Law': 'LAW',
    'Arts': 'ART',
    'Design': 'DES',
    'Media': 'MEDA',
    'Government': 'GOV',
    'Agriculture': 'AGR',
    'Environment': 'ENV',
    'Sports': 'SPT',
    'Hospitality': 'HOSP',
    'Aviation': 'AVI',
    'Manufacturing': 'MFG',
    'Construction': 'CONS',
    'Skilled Trades': 'TRD',
    'Transportation': 'TRN',
    'Psychology and Social Sciences': 'PSY',
    'Psychology And Social Sciences': 'PSY',
    'Education': 'EDU',
    'Biotechnology': 'BIO',
    'Pharmaceuticals': 'PHAR',
    'Defence and Security': 'DEF',
    'Defence And Security': 'DEF',
    'Fashion': 'FASH',
    'Food': 'FOOD',
    'Real Estate': 'REST',
    'Emerging Careers': 'EMG',
    'Interdisciplinary': 'INT'
}

ABILITY_COLUMNS = {
    'Mathematical_Ability_Requirement': 'Mathematical Reasoning',
    'Logical_Reasoning_Requirement': 'Logical Analysis',
    'Scientific_Reasoning_Requirement': 'Scientific Method & Investigation',
    'Problem_Solving_Requirement': 'Complex Problem Solving',
    'Analytical_Ability_Requirement': 'Analytical Thinking',
    'Critical_Thinking_Requirement': 'Critical Evaluation',
    'Communication_Requirement': 'Communication & Articulation',
    'Creativity_Requirement': 'Creative Ideation & Innovation',
    'Digital_Ability_Requirement': 'Digital Technology Fluency',
    'Programming_Ability_Requirement': 'Software & Algorithm Design',
    'Spatial_Ability_Requirement': 'Spatial Visualization',
    'Practical_Ability_Requirement': 'Hands-on Technical Execution',
    'Observation_Ability_Requirement': 'Detailed Observation',
    'Decision_Making_Requirement': 'Strategic Decision Making',
    'Learning_Ability_Requirement': 'Continuous Learning & Adaptability',
    'Leadership_Requirement': 'Leadership & Direction',
    'Teamwork_Requirement': 'Team Collaboration'
}

SUBJECT_COLUMNS = {
    'Subject_Mathematics_Importance': 'Mathematics',
    'Subject_Physics_Importance': 'Physics',
    'Subject_Chemistry_Importance': 'Chemistry',
    'Subject_Biology_Importance': 'Biology',
    'Subject_Computer_Importance': 'Computer Science',
    'Subject_English_Importance': 'English',
    'Subject_SocialScience_Importance': 'Social Science',
    'Subject_Economics_Importance': 'Economics',
    'Subject_Accountancy_Importance': 'Accountancy',
    'Subject_BusinessStudies_Importance': 'Business Studies',
    'Subject_History_Importance': 'History',
    'Subject_PoliticalScience_Importance': 'Political Science',
    'Subject_Psychology_Importance': 'Psychology',
    'Subject_Art_Importance': 'Fine Arts & Design'
}

IMPORTANCE_LABELS = {
    5: 'Critical',
    4: 'Very High',
    3: 'High',
    2: 'Moderate',
    1: 'Basic'
}


def normalize_text(text: str) -> str:
    """Cleans and standardizes text strings with proper title casing."""
    if not text:
        return ''
    cleaned = ' '.join(str(text).strip().split())
    words = cleaned.split()
    result = []
    for w in words:
        upper = w.upper()
        lower = w.lower()
        if upper in ['AI', 'IT', 'UI', 'UX', 'CAD', 'CAM', 'VFX', '3D', '2D', 'CA', 'IAS', 'IPS', 'IFS', 'GIS', 'CFO', 'CEO', 'CTO', 'SOC', 'SEO', 'NEET', 'JEE', 'CLAT', 'UPSC', 'MBBS', 'BCA', 'MCA', 'BBA', 'MBA']:
            result.append(upper)
        elif lower in ['and', '&', 'of', 'in', 'the', 'for', 'to', 'with', 'on', 'at', 'by', 'a', 'an']:
            result.append(lower if len(result) > 0 else w.capitalize())
        else:
            result.append(w.capitalize())
    return ' '.join(result)


def parse_numeric(value, default=0) -> int:
    """Safely converts numeric values to integer bounded 0..5."""
    try:
        val = int(round(float(value)))
        return max(0, min(5, val))
    except (ValueError, TypeError):
        return default


def generate_career_code(domain_name: str, cid_raw: str, index: int) -> str:
    """Generates a deterministic, standard career code."""
    prefix = DOMAIN_CODES.get(domain_name, 'GEN')
    clean_cid = re.sub(r'[^0-9A-Za-z]', '', cid_raw)
    if clean_cid.startswith('CID'):
        clean_cid = clean_cid[3:]
    if clean_cid:
        return f"CAR-{prefix}-{clean_cid}"
    return f"CAR-{prefix}-{index:04d}"


def run_career_import_pipeline():
    """Main execution function for importing and normalizing the career dataset."""
    csv_path = BASE_DIR / 'data' / 'Career_Knowledge_Requirements_Raw.csv'
    if not csv_path.exists():
        alt_path = Path('C:/Users/arjun/Downloads/Career_Knowledge_Requirements_Raw.csv')
        if alt_path.exists():
            csv_path = alt_path
        else:
            print(f"Error: Dataset file not found at {csv_path}")
            return

    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', 'abc123')
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    db_name = os.getenv('DB_NAME', 'career_recommendation_db')

    print(f"Connecting to MySQL Server at {host}:{port} -> Database: {db_name}...")
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=db_name,
        autocommit=False
    )
    cursor = conn.cursor()

    print(f"Reading CSV dataset from {csv_path.name}...")
    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    rows_read = len(all_rows)
    invalid_rows = 0
    duplicate_rows = 0
    careers_imported = 0
    domains_imported = 0
    subdomains_imported = 0
    clusters_imported = 0
    skills_imported = 0
    subjects_imported = 0
    education_imported = 0
    pathways_imported = 0

    # Step 1: Pre-process and deduplicate careers by canonical key
    careers_to_import = {}
    
    for r in all_rows:
        raw_name = r.get('Career_Name', '').strip()
        raw_dom = r.get('Career_Domain', '').strip()
        raw_sub = r.get('Career_Subdomain', '').strip()
        raw_clu = r.get('Career_Cluster', '').strip()
        cid = r.get('Career_ID', '').strip()

        if not raw_name or raw_name.lower() in ['unknown', 'n/a', 'na', 'none', 'null', 'test']:
            invalid_rows += 1
            continue

        c_name = normalize_text(raw_name)
        c_dom = normalize_text(raw_dom) if raw_dom.upper() not in ['UNKNOWN', 'N/A', 'NA', 'NOT APPLICABLE', 'NOT AVAILABLE', ''] else 'Interdisciplinary'
        c_sub = normalize_text(raw_sub) if raw_sub.upper() not in ['UNKNOWN', 'N/A', 'NA', ''] else 'General'
        c_clu = normalize_text(raw_clu) if raw_clu.upper() not in ['UNKNOWN', 'N/A', 'NA', ''] else 'General Practice'

        canon_key = (c_dom, c_name)

        if canon_key in careers_to_import:
            duplicate_rows += 1
            continue

        careers_to_import[canon_key] = {
            'cid': cid,
            'name': c_name,
            'domain': c_dom,
            'subdomain': c_sub,
            'cluster': c_clu,
            'row': r
        }

    print(f"Pre-processing complete: {rows_read} rows read -> {len(careers_to_import)} unique careers identified.")

    try:
        # Step 2: Fetch or Create Career Domains
        cursor.execute("SELECT id, domain_name FROM career_domains;")
        existing_domains = {name: did for did, name in cursor.fetchall()}

        domain_order = len(existing_domains) + 1
        for canon_key, cdata in careers_to_import.items():
            dom_name = cdata['domain']
            if dom_name not in existing_domains:
                icon = DOMAIN_ICONS.get(dom_name, 'bi-briefcase')
                cursor.execute(
                    "INSERT INTO career_domains (domain_name, description, icon, display_order, is_active) "
                    "VALUES (%s, %s, %s, %s, TRUE) "
                    "ON DUPLICATE KEY UPDATE display_order=VALUES(display_order);",
                    (dom_name, f"Careers and professional pathways in {dom_name}.", icon, domain_order)
                )
                dom_id = cursor.lastrowid
                if not dom_id:
                    cursor.execute("SELECT id FROM career_domains WHERE domain_name = %s;", (dom_name,))
                    dom_id = cursor.fetchone()[0]
                existing_domains[dom_name] = dom_id
                domain_order += 1
                domains_imported += 1

        # Step 3: Fetch or Create Subdomains
        cursor.execute("SELECT id, domain_id, name FROM career_subdomains;")
        existing_subdomains = {(did, name): sid for sid, did, name in cursor.fetchall()}

        for canon_key, cdata in careers_to_import.items():
            dom_id = existing_domains[cdata['domain']]
            sub_name = cdata['subdomain']
            sub_key = (dom_id, sub_name)

            if sub_key not in existing_subdomains:
                cursor.execute(
                    "INSERT INTO career_subdomains (domain_id, name, description) "
                    "VALUES (%s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE description=VALUES(description);",
                    (dom_id, sub_name, f"Specialized focus area in {sub_name}.")
                )
                sub_id = cursor.lastrowid
                if not sub_id:
                    cursor.execute("SELECT id FROM career_subdomains WHERE domain_id=%s AND name=%s;", (dom_id, sub_name))
                    sub_id = cursor.fetchone()[0]
                existing_subdomains[sub_key] = sub_id
                subdomains_imported += 1

        # Step 4: Fetch or Create Clusters
        cursor.execute("SELECT id, subdomain_id, name FROM career_clusters;")
        existing_clusters = {(sid, name): clid for clid, sid, name in cursor.fetchall()}

        for canon_key, cdata in careers_to_import.items():
            dom_id = existing_domains[cdata['domain']]
            sub_id = existing_subdomains[(dom_id, cdata['subdomain'])]
            clu_name = cdata['cluster']
            clu_key = (sub_id, clu_name)

            if clu_key not in existing_clusters:
                cursor.execute(
                    "INSERT INTO career_clusters (subdomain_id, name, description) "
                    "VALUES (%s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE description=VALUES(description);",
                    (sub_id, clu_name, f"Occupational cluster for {clu_name}.")
                )
                clu_id = cursor.lastrowid
                if not clu_id:
                    cursor.execute("SELECT id FROM career_clusters WHERE subdomain_id=%s AND name=%s;", (sub_id, clu_name))
                    clu_id = cursor.fetchone()[0]
                existing_clusters[clu_key] = clu_id
                clusters_imported += 1

        # Step 5: Import Careers, Skills, Subjects, Education & Pathways
        used_codes = set()
        cursor.execute("SELECT career_code FROM careers;")
        for (code,) in cursor.fetchall():
            used_codes.add(code)

        career_index = 1000
        for canon_key, cdata in careers_to_import.items():
            dom_id = existing_domains[cdata['domain']]
            sub_id = existing_subdomains[(dom_id, cdata['subdomain'])]
            clu_id = existing_clusters[(sub_id, cdata['cluster'])]
            r = cdata['row']
            c_name = cdata['name']

            code = generate_career_code(cdata['domain'], cdata['cid'], career_index)
            if code in used_codes:
                code = f"{code}-{career_index}"
            used_codes.add(code)
            career_index += 1

            desc = r.get('Career_Description', '').strip() or f"Professional role working as a {c_name} in {cdata['domain']}."
            min_edu = r.get('Minimum_Education_Level', '').strip() or "Bachelor's Degree"
            typ_edu = r.get('Typical_Education_Level', '').strip() or r.get('Preferred_Degree', '').strip() or "Relevant Undergraduate Degree"
            preferred_deg = r.get('Preferred_Degree', '').strip()
            if preferred_deg and preferred_deg.lower() not in ['not specified', 'none', 'n/a']:
                typ_edu = f"{typ_edu} ({preferred_deg})"
            
            work_env = r.get('Work_Environment', '').strip() or "Professional Workplace"
            work_style = r.get('Work_Setting', '').strip() or "Structured / Team"
            pathway_text = r.get('Career_Pathway', '').strip() or f"{min_edu} -> {typ_edu} -> {c_name}"
            entry_role = r.get('Entry_Level_Role', '').strip() or f"Junior {c_name}"
            adv_role = r.get('Advanced_Role', '').strip() or f"Senior {c_name} / Lead Specialist"
            
            related_list = []
            for rc_col in ['Related_Career_1', 'Related_Career_2', 'Related_Career_3']:
                rc_val = r.get(rc_col, '').strip()
                if rc_val and rc_val.lower() not in ['none', 'n/a', 'unknown', '']:
                    related_list.append(rc_val)
            related_careers_str = ', '.join(related_list) if related_list else f"Senior {c_name}"

            top_subjects = []
            for scol, sname in SUBJECT_COLUMNS.items():
                imp = parse_numeric(r.get(scol, 0))
                if imp >= 3:
                    top_subjects.append(sname)
            preferred_subj_str = ', '.join(top_subjects) if top_subjects else "General Academic Subjects"

            cursor.execute(
                """
                INSERT INTO careers (
                    career_code, career_name, domain_id, subdomain_id, cluster_id,
                    description, minimum_education, typical_education,
                    work_environment, work_style, entry_level_role,
                    advanced_role, related_careers, is_active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
                ON DUPLICATE KEY UPDATE
                    domain_id=VALUES(domain_id),
                    subdomain_id=VALUES(subdomain_id),
                    cluster_id=VALUES(cluster_id),
                    description=VALUES(description),
                    minimum_education=VALUES(minimum_education),
                    typical_education=VALUES(typical_education),
                    work_environment=VALUES(work_environment),
                    work_style=VALUES(work_style),
                    entry_level_role=VALUES(entry_level_role),
                    advanced_role=VALUES(advanced_role),
                    related_careers=VALUES(related_careers);
                """,
                (
                    code, c_name, dom_id, sub_id, clu_id,
                    desc, min_edu, typ_edu,
                    work_env, work_style, entry_role,
                    adv_role, related_careers_str
                )
            )
            career_id = cursor.lastrowid
            if not career_id:
                cursor.execute("SELECT id FROM careers WHERE career_code=%s;", (code,))
                career_id = cursor.fetchone()[0]

            careers_imported += 1

            # Insert Skills
            for acol, sname in ABILITY_COLUMNS.items():
                lvl = parse_numeric(r.get(acol, 0))
                if lvl >= 1:
                    lbl = IMPORTANCE_LABELS.get(lvl, 'High')
                    cursor.execute(
                        """
                        INSERT INTO career_skills (career_id, skill_name, importance_level, importance_label)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE importance_level=VALUES(importance_level), importance_label=VALUES(importance_label);
                        """,
                        (career_id, sname, lvl, lbl)
                    )
                    skills_imported += 1

            # Insert Subjects
            for scol, sname in SUBJECT_COLUMNS.items():
                lvl = parse_numeric(r.get(scol, 0))
                if lvl >= 1:
                    lbl = IMPORTANCE_LABELS.get(lvl, 'High')
                    cursor.execute(
                        """
                        INSERT INTO career_subjects (career_id, subject_name, importance_level, importance_label)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE importance_level=VALUES(importance_level), importance_label=VALUES(importance_label);
                        """,
                        (career_id, sname, lvl, lbl)
                    )
                    subjects_imported += 1

            # Insert Education Milestones (5 Steps)
            edu_milestones = [
                (1, 'Secondary Education', 'Class 10 Secondary Education', f"Foundational focus on {preferred_subj_str} and problem solving."),
                (2, 'Higher Secondary', 'Class 11-12 Higher Secondary', f"Target stream alignment in {cdata['domain']} with elective coursework."),
                (3, 'Undergraduate / Foundational', min_edu, f"Foundational qualification: {preferred_deg or min_edu}."),
                (4, 'Professional Specialization', typ_edu, f"Advanced degree or training for {c_name}."),
                (5, 'Career Entry & Practice', entry_role, f"Entry-level professional practice transitioning into {adv_role}.")
            ]

            cursor.execute("DELETE FROM career_education WHERE career_id=%s;", (career_id,))
            for seq, lvl_name, deg_name, ed_desc in edu_milestones:
                cursor.execute(
                    """
                    INSERT INTO career_education (career_id, education_level, degree_name, description, sequence_order)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (career_id, lvl_name, deg_name, ed_desc, seq)
                )
                education_imported += 1

            # Insert Career Pathways (3 Stages)
            stages = [
                (1, 'Foundation Stage', f"Start as {entry_role} mastering operational duties and core workflows."),
                (2, 'Professional Mastery', f"Advance to {c_name} leading independent projects and technical execution."),
                (3, 'Leadership & Executive', f"Progress into {adv_role} directing strategy, mentorship, and high-impact initiatives.")
            ]
            cursor.execute("DELETE FROM career_pathways WHERE career_id=%s;", (career_id,))
            for stg_num, stg_name, stg_desc in stages:
                cursor.execute(
                    """
                    INSERT INTO career_pathways (career_id, stage_number, stage_name, description)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (career_id, stg_num, stg_name, stg_desc)
                )
                pathways_imported += 1

        # Commit transaction atomically
        conn.commit()

        print("\n" + "=" * 65)
        print("  CAREER KNOWLEDGE DATASET IMPORT REPORT")
        print("=" * 65)
        print(f"  Rows Read:                       {rows_read:,}")
        print(f"  Invalid Records Rejected:        {invalid_rows:,}")
        print(f"  Duplicate Records Detected:      {duplicate_rows:,}")
        print(f"  --------------------------------------------------")
        print(f"  Careers Imported / Updated:      {careers_imported:,}")
        print(f"  Domains Registered:              {len(existing_domains):,} (+{domains_imported} new)")
        print(f"  Subdomains Registered:           {len(existing_subdomains):,} (+{subdomains_imported} new)")
        print(f"  Clusters Registered:             {len(existing_clusters):,} (+{clusters_imported} new)")
        print(f"  Career Skills Mapped:            {skills_imported:,}")
        print(f"  Career Subjects Mapped:          {subjects_imported:,}")
        print(f"  Education Milestones Created:    {education_imported:,}")
        print(f"  Career Progression Stages:       {pathways_imported:,}")
        print("=" * 65)
        print("[OK] SUCCESS: Career knowledge dataset import completed with full relational integrity!")

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Error during import pipeline: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    run_career_import_pipeline()
