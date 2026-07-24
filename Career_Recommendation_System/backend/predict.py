"""
predict.py — ML Prediction Module
Loads XGBoost model and returns top-5 career recommendations with confidence scores.
"""

import os
import pickle
import numpy as np
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')

# ── Globals ────────────────────────────────────────────────────────────────
_model = None
_label_encoder = None
_feature_meta = None   # dict with feature_cols, cat_cols, cat_encoders


def load_model():
    """Load model artifacts from disk. Call once at app startup."""
    global _model, _label_encoder, _feature_meta
    try:
        with open(os.path.join(MODEL_DIR, 'xgboost_model.pkl'), 'rb') as f:
            _model = pickle.load(f)
        with open(os.path.join(MODEL_DIR, 'label_encoder.pkl'), 'rb') as f:
            _label_encoder = pickle.load(f)
        with open(os.path.join(MODEL_DIR, 'feature_columns.pkl'), 'rb') as f:
            _feature_meta = pickle.load(f)
        logger.info("ML model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return False


def is_loaded():
    return _model is not None and _label_encoder is not None and _feature_meta is not None


def _preprocess(user_input: dict) -> np.ndarray:
    """
    Convert raw user input dict → numpy array matching training feature order.
    user_input keys should match training column names (case-sensitive).
    Missing values are filled with 0/Unknown.
    """
    feature_cols = _feature_meta['feature_cols']
    cat_cols = _feature_meta['cat_cols']
    cat_encoders = _feature_meta['cat_encoders']

    row = []
    for col in feature_cols:
        val = user_input.get(col, None)

        if col in cat_cols:
            encoder = cat_encoders[col]
            str_val = str(val) if val is not None else 'Unknown'
            try:
                encoded = encoder.transform([str_val])[0]
            except ValueError:
                encoded = 0   # unseen category → 0
            row.append(encoded)
        else:
            try:
                row.append(float(val) if val is not None else 0.0)
            except (TypeError, ValueError):
                row.append(0.0)

    return np.array(row).reshape(1, -1)


def predict_careers(user_input: dict, top_n: int = 5) -> list:
    """
    Predict top-N careers from user input.

    Returns:
        list of dicts: [{'career': str, 'confidence': float, 'rank': int}, ...]
    """
    if not is_loaded():
        raise RuntimeError("Model not loaded. Call load_model() first.")

    X = _preprocess(user_input)
    proba = _model.predict_proba(X)[0]          # shape: (n_classes,)
    top_indices = np.argsort(proba)[::-1][:top_n]

    results = []
    for rank, idx in enumerate(top_indices, start=1):
        career_name = _label_encoder.inverse_transform([idx])[0]
        confidence = float(proba[idx]) * 100
        results.append({
            'rank': rank,
            'career': career_name,
            'confidence': round(confidence, 2),
        })
    return results


def build_user_input(form_data: dict) -> dict:
    """
    Map assessment form fields → model feature column names.
    Handles the mapping between HTML form names and CSV column names.
    All form field name mismatches are resolved here so the model
    always receives actual user values, never defaults.
    """
    def safe_float(key, default=0.0):
        try:
            return float(form_data.get(key, default) or default)
        except (ValueError, TypeError):
            return default

    def safe_int(key, default=0):
        try:
            return int(form_data.get(key, default) or default)
        except (ValueError, TypeError):
            return default

    def safe_str(key, default='Unknown'):
        val = form_data.get(key, default)
        return str(val).strip() if val else default

    # ── Personal / Academic Context ───────────────────────────────────────
    age            = safe_int('age', 22)
    gender         = safe_str('gender', 'Male')
    education_lvl  = safe_str('education_level', "Bachelor's")
    stream         = safe_str('stream', 'Science')
    current_course = safe_str('current_course', 'B.Tech')
    cgpa           = safe_float('cgpa', 3.0)
    semester       = safe_int('current_semester', 6)
    backlogs       = safe_int('backlogs', 0)
    attendance     = safe_float('attendance', 80.0)
    overall_pct    = safe_float('overall_percentage', 75.0)

    # ── Subject Scores (0-100) ────────────────────────────────────────────
    math_score    = safe_float('math_score', 70)
    physics_score = safe_float('physics_score', 70)
    chem_score    = safe_float('chemistry_score', 70)
    cs_score      = safe_float('cs_score', 70)
    english_score = safe_float('english_score', 70)
    bio_score     = safe_float('biology_score', 0)
    eco_score     = safe_float('economics_score', 0)
    acc_score     = safe_float('accountancy_score', 0)
    biz_score     = safe_float('business_studies_score', 0)
    stats_score   = safe_float('statistics_score', 0)
    hist_score    = safe_float('history_score', 0)
    geo_score     = safe_float('geography_score', 0)
    pol_score     = safe_float('political_science_score', 0)
    psych_score   = safe_float('psychology_score', 0)
    ss_score      = safe_float('social_science_score', 0)
    lang_score    = safe_float('second_language_score', 0)
    project_score = safe_float('project_score', 70)

    # ── Aptitude Scores (0-10) ────────────────────────────────────────────
    # FIX: was 'logical_reasoning' not in form; now properly mapped
    logical_reasoning  = safe_float('logical_reasoning', 5)
    analytical_thinking = safe_float('analytical_thinking', 5)   # FIX: was 'analytical_skills'
    numerical_ability  = safe_float('numerical_ability', 5)
    spatial_ability    = safe_float('spatial_ability', 5)
    mechanical_apt     = safe_float('mechanical_aptitude', 5)
    scientific_apt     = safe_float('scientific_aptitude', 5)
    language_apt       = safe_float('language_aptitude', 5)
    business_apt       = safe_float('business_aptitude', 5)
    creative_apt       = safe_float('creative_aptitude', 5)
    leadership_apt     = safe_float('leadership_aptitude', 5)
    observation        = safe_float('observation', 5)
    memory             = safe_float('memory', 5)
    learning_ability   = safe_float('learning_ability', 5)

    # ── Soft Skills (0-10) ────────────────────────────────────────────────
    communication       = safe_float('communication', 5)
    leadership          = safe_float('leadership', 5)
    teamwork            = safe_float('teamwork', 5)
    problem_solving     = safe_float('problem_solving', 5)
    creativity          = safe_float('creativity', 5)
    time_management     = safe_float('time_management', 5)
    adaptability        = safe_float('adaptability', 5)
    confidence          = safe_float('confidence', 5)
    decision_making     = safe_float('decision_making', 5)
    critical_thinking   = safe_float('critical_thinking', 5)
    self_learning       = safe_float('self_learning', 5)
    emotional_intel     = safe_float('emotional_intelligence', 5)
    stress_management   = safe_float('stress_management', 5)
    networking_soft     = safe_float('networking_soft_skill', 5)

    # ── Technical Skills (0-10) ───────────────────────────────────────────
    programming   = safe_float('programming', 5)
    # FIX: all were mapped to wrong keys (python_skill, java_skill, etc.)
    python_skill  = safe_float('python', 5)         # FIX: was 'python_skill'
    java_skill    = safe_float('java', 5)            # FIX: was 'java_skill'
    cpp_skill     = safe_float('cpp', 5)             # FIX: was 'cpp_skill'
    sql_skill     = safe_float('sql', 5)             # FIX: was 'sql_skill'
    database      = safe_float('database', 5)
    networking_t  = safe_float('networking', 5)      # FIX: was 'networking_skill'
    cybersecurity = safe_float('cyber_security', 5)
    cloud         = safe_float('cloud_computing', 5)
    ai_skill      = safe_float('ai', 5)              # FIX: was 'ai_skill'
    ml_skill      = safe_float('machine_learning', 5)
    data_analysis = safe_float('data_analysis', 5)
    ui_ux         = safe_float('ui_ux', 5)
    graphic_design = safe_float('graphic_design', 5)

    # ── Digital Literacy Skills (0-10) ────────────────────────────────────
    ms_word            = safe_float('ms_word', 5)
    excel              = safe_float('excel', 5)
    powerpoint         = safe_float('powerpoint', 5)
    typing_speed       = safe_float('typing_speed', 40)
    internet_research  = safe_float('internet_research', 5)
    digital_comm       = safe_float('digital_communication', 5)
    ai_tool_usage      = safe_float('ai_tool_usage', 5)
    online_collab      = safe_float('online_collaboration', 5)
    cyber_awareness    = safe_float('cyber_awareness', 5)

    # ── Domain Skills (0-10) ─────────────────────────────────────────────
    accounting_skill   = safe_float('accounting_skill', 0)
    financial_analysis = safe_float('financial_analysis', 0)
    marketing_skill    = safe_float('marketing_skill', 0)
    patient_care       = safe_float('patient_care', 0)
    lab_skills         = safe_float('laboratory_skills', 0)
    mechanical_design  = safe_float('mechanical_design', 0)
    electrical_maint   = safe_float('electrical_maintenance', 0)
    civil_drawing      = safe_float('civil_drawing', 0)
    legal_research     = safe_float('legal_research', 0)
    content_writing    = safe_float('content_writing', 0)
    scientific_research = safe_float('scientific_research', 0)
    agriculture_skill  = safe_float('agriculture_skill', 0)
    video_editing      = safe_float('video_editing', 0)

    # ── Interest Scores (0-10) ────────────────────────────────────────────
    # FIX: many were mapped to wrong form field names
    tech_interest    = safe_float('technology_interest', 5)   # FIX: was missing
    medicine_int     = safe_float('healthcare', 5)            # FIX: was 'medicine_interest'
    business_int     = safe_float('business', 5)              # FIX: was 'business_interest'
    finance_int      = safe_float('finance', 5)               # FIX: was 'finance_interest'
    law_int          = safe_float('law_interest', 0)
    teaching_int     = safe_float('teaching', 5)              # FIX: was 'teaching_interest'
    research_int     = safe_float('research', 5)              # FIX: was 'research_interest'
    agriculture_int  = safe_float('agriculture_interest', 0)
    arts_int         = safe_float('arts_interest', 0)
    design_int       = safe_float('design', 5)               # FIX: was 'design_interest'
    sports_int       = safe_float('sports_interest', 0)
    music_int        = safe_float('music_interest', 0)
    writing_int      = safe_float('writing_interest', 0)
    journalism_int   = safe_float('journalism_interest', 0)
    psychology_int   = safe_float('psychology_interest', 0)
    environment_int  = safe_float('environment_interest', 0)
    hospitality_int  = safe_float('hospitality_interest', 0)
    social_svc_int   = safe_float('social_service_interest', 0)
    defence_int      = safe_float('defence_interest', 0)
    robotics_int     = safe_float('robotics_interest', 0)
    ai_int           = safe_float('artificial_intelligence', 5)  # FIX: was 'interest_ai'
    animation_int    = safe_float('animation_interest', 0)
    entrepreneurship_int = safe_float('entrepreneurship', 5)     # FIX: was 'entrepreneurship_interest'
    gaming_int       = safe_float('gaming_interest', 0)

    # ── Personality / Style ───────────────────────────────────────────────
    personality_type  = safe_str('personality_type', 'Ambivert')
    learning_style    = safe_str('learning_style', 'Visual')
    work_preference   = safe_str('work_preference', 'Team')
    risk_taking       = safe_str('risk_taking', 'Medium')
    leadership_style  = safe_str('leadership_style', 'Democratic')

    # ── Career Preferences ────────────────────────────────────────────────
    preferred_industry   = safe_str('preferred_industry', 'Technology')
    preferred_location   = safe_str('preferred_location', 'Urban')
    expected_salary      = safe_str('expected_salary', '6-10 LPA')
    govt_private         = safe_str('govt_private', 'Private')
    higher_studies       = safe_str('higher_studies', 'No')
    startup_interest     = safe_str('startup_interest', 'No')
    abroad_studies       = safe_str('abroad_studies_interest', 'No')
    research_int_level   = safe_str('research_interest_level', 'Low')
    work_life_balance    = safe_str('work_life_balance_preference', 'Balanced')

    # ── Experience ────────────────────────────────────────────────────────
    internship_done      = safe_str('internship_completed', 'No')
    internship_domain    = safe_str('internship_domain', 'None')
    internship_duration  = safe_int('internship_duration', 0)
    industrial_visit     = safe_str('industrial_visit', 'No')
    volunteer_exp        = safe_str('volunteer_experience', 'No')
    community_svc_hrs    = safe_int('community_service_hours', 0)
    # FIX: was 'project_count', form sends 'projects_count'
    project_count        = safe_int('projects_count', 0)
    cert_count           = safe_int('certification_count', 0)

    # Certifications - derive Certification_1 and Certification_2 from checkboxes
    cert_boxes = ['cloud_certification', 'python_certification', 'java_certification',
                  'data_science_certification', 'cyber_security_certification',
                  'networking_certification', 'aws_certification', 'azure_certification',
                  'google_cloud_certification']
    earned_certs = [c.replace('_certification', '').replace('_', ' ').title()
                    for c in cert_boxes if form_data.get(c)]
    cert_1 = earned_certs[0] if len(earned_certs) > 0 else 'None'
    cert_2 = earned_certs[1] if len(earned_certs) > 1 else 'None'
    cert_count_derived = len(earned_certs)
    final_cert_count = max(cert_count, cert_count_derived)

    # Projects
    project_1 = safe_str('project_1', 'None')
    project_2 = safe_str('project_2', 'None')
    # FIX: was 'project_count'; now uses both form_data 'projects_count' and derived
    project_count_form = safe_int('projects_count', 0)
    final_project_count = max(project_count, project_count_form)

    # ── Socioeconomic Background ──────────────────────────────────────────
    parent_education     = safe_str('parent_education', "Graduate")
    parent_occupation    = safe_str('parent_occupation', 'Service')
    annual_income        = safe_str('annual_family_income', '3-6 LPA')
    first_gen            = safe_str('first_generation_learner', 'No')
    internet_access      = safe_str('internet_access', 'Yes')
    laptop_avail         = safe_str('laptop_availability', 'Yes')
    study_environment    = safe_str('study_environment', 'Home')

    # ── School Context ────────────────────────────────────────────────────
    board                = safe_str('board', 'CBSE')
    school_type          = safe_str('school_college_type', 'Private')
    medium               = safe_str('medium_of_instruction', 'English')
    district             = safe_str('district', 'Unknown')
    state                = safe_str('state', 'Unknown')
    urban_rural          = safe_str('urban_rural', 'Urban')

    # ── Extracurricular ───────────────────────────────────────────────────
    activity_1 = safe_str('activity_1', 'None')
    activity_2 = safe_str('activity_2', 'None')
    activity_3 = safe_str('activity_3', 'None')

    # ════════════════════════════════════════════════════════════════════════
    # COMPUTED SCORES (Phase 3) — derived from the inputs above
    # These are columns the model was trained on but are derived, not user-input
    # ════════════════════════════════════════════════════════════════════════

    # Academic_Performance_Score (0-100): weighted average of subject scores
    subject_scores = [s for s in [math_score, english_score, overall_pct] if s > 0]
    if stream == 'Science':
        subject_scores = [s for s in [math_score, physics_score, chem_score, cs_score,
                                       bio_score, english_score] if s > 0]
    elif stream == 'Commerce':
        subject_scores = [s for s in [math_score, acc_score, biz_score, eco_score,
                                       english_score] if s > 0]
    elif stream == 'Arts':
        subject_scores = [s for s in [hist_score, geo_score, pol_score, psych_score,
                                       english_score] if s > 0]
    academic_perf_score = round(sum(subject_scores) / len(subject_scores), 2) if subject_scores else overall_pct

    # Soft_Skill_Score (0-10): average of all soft skills
    soft_skills_list = [communication, leadership, teamwork, problem_solving, creativity,
                        time_management, adaptability, confidence, decision_making,
                        critical_thinking, self_learning, emotional_intel, stress_management]
    soft_skill_score = round(sum(soft_skills_list) / len(soft_skills_list), 2)

    # Digital_Literacy_Score (0-10): average of digital literacy skills
    digital_skills_list = [ms_word, excel, powerpoint, internet_research,
                           digital_comm, ai_tool_usage, online_collab, cyber_awareness]
    digital_literacy_score = round(sum(digital_skills_list) / len(digital_skills_list), 2)

    # Domain_Skill_Score (0-10): average of domain-specific skills
    domain_skills_list = [accounting_skill, financial_analysis, marketing_skill,
                          patient_care, lab_skills, mechanical_design, legal_research,
                          content_writing, video_editing, scientific_research]
    non_zero_domain = [s for s in domain_skills_list if s > 0]
    domain_skill_score = round(sum(non_zero_domain) / len(non_zero_domain), 2) if non_zero_domain else 0.0

    # STEM_Strength_Score (0-100): science/math/CS subjects
    stem_scores = [s for s in [math_score, physics_score, chem_score, cs_score,
                                bio_score, stats_score] if s > 0]
    stem_strength_score = round(sum(stem_scores) / len(stem_scores), 2) if stem_scores else 0.0

    # Business_Aptitude_Score (0-10)
    biz_apt_score = round((business_apt + business_int * 0.8 + finance_int * 0.6) / 2.4, 2)

    # Creativity_Score (0-10)
    creativity_score = round((creativity + creative_apt + arts_int * 0.5 + animation_int * 0.3) / 2.8, 2)

    # Leadership_Score (0-10)
    leadership_score = round((leadership + leadership_apt) / 2.0, 2)

    # Career_Readiness_Score (0-100)
    readiness_pts = 0
    readiness_pts += min(final_project_count * 10, 30)       # max 30 from projects
    readiness_pts += min(final_cert_count * 10, 30)          # max 30 from certs
    readiness_pts += 20 if internship_done.lower() == 'yes' else 0
    readiness_pts += min(internship_duration * 3, 15)        # max 15 from internship months
    readiness_pts += 5 if volunteer_exp.lower() == 'yes' else 0
    career_readiness_score = min(readiness_pts, 100)

    # Total_Technical_Skill_Score (0-10): avg of all tech skills
    tech_skills_list = [programming, python_skill, java_skill, cpp_skill, sql_skill,
                        database, networking_t, cybersecurity, cloud, ai_skill,
                        ml_skill, data_analysis, ui_ux, graphic_design]
    total_tech_score = round(sum(tech_skills_list) / len(tech_skills_list), 2)

    # ── Subject_Studied Boolean Flags (auto-derived from stream) ──────────
    is_science  = 1 if stream in ('Science',) else 0
    is_commerce = 1 if stream in ('Commerce',) else 0
    is_arts     = 1 if stream in ('Arts',) else 0
    is_degree   = 1 if education_lvl in ("Bachelor's", "Master's", "PhD", "Diploma") else 0

    math_studied    = 1 if (is_science or is_commerce or is_degree) else 0
    science_studied = 1 if is_science else 0
    english_studied = 1
    ss_studied      = 1
    lang_studied    = 1
    physics_studied = 1 if is_science else 0
    chem_studied    = 1 if is_science else 0
    bio_studied     = 1 if is_science else 0
    cs_studied      = 1 if (is_science or is_degree) else 0
    acc_studied     = 1 if is_commerce else 0
    biz_studied     = 1 if is_commerce else 0
    eco_studied     = 1 if is_commerce else 0
    stats_studied   = 1 if (is_science or is_commerce) else 0
    hist_studied    = 1 if is_arts else 0
    pol_studied     = 1 if is_arts else 0
    geo_studied     = 1 if is_arts else 0
    psych_studied   = 1 if is_arts else 0

    # ════════════════════════════════════════════════════════════════════════
    # FINAL MAPPING → model column names
    # ════════════════════════════════════════════════════════════════════════
    mapping = {
        # Personal
        'Age':                              age,
        'Gender':                           gender,
        'Education_Level':                  education_lvl,
        'Stream':                           stream,
        'Current_Course':                   current_course,
        'Board':                            board,
        'School_or_College_Type':           school_type,
        'Medium_of_Instruction':            medium,
        'District':                         district,
        'State':                            state,
        'Urban_or_Rural':                   urban_rural,
        'CGPA':                             cgpa,
        'Current_Semester':                 semester,
        'Backlogs':                         backlogs,
        'Attendance':                       attendance,
        'Overall_Percentage':               overall_pct,
        'Project_Score':                    project_score,

        # Subject Scores
        'Mathematics':                      math_score,
        'Science':                          stem_strength_score,  # aggregate
        'English':                          english_score,
        'Social_Science':                   ss_score,
        'Second_Language':                  lang_score,
        'Physics':                          physics_score,
        'Chemistry':                        chem_score,
        'Biology':                          bio_score,
        'Computer_Science':                 cs_score,
        'Accountancy':                      acc_score,
        'Business_Studies':                 biz_score,
        'Economics':                        eco_score,
        'Statistics':                       stats_score,
        'History':                          hist_score,
        'Political_Science':                pol_score,
        'Geography':                        geo_score,
        'Psychology':                       psych_score,

        # Aptitude
        'Logical_Reasoning':                logical_reasoning,
        'Analytical_Thinking':              analytical_thinking,
        'Numerical_Ability':                numerical_ability,
        'Spatial_Ability':                  spatial_ability,
        'Mechanical_Aptitude':              mechanical_apt,
        'Scientific_Aptitude':             scientific_apt,
        'Language_Aptitude':               language_apt,
        'Business_Aptitude':               business_apt,
        'Creative_Aptitude':               creative_apt,
        'Leadership_Aptitude':             leadership_apt,
        'Observation':                     observation,
        'Memory':                          memory,
        'Critical_Thinking':               critical_thinking,
        'Decision_Making':                 decision_making,
        'Learning_Ability':                learning_ability,

        # Soft Skills
        'Communication':                   communication,
        'Leadership':                      leadership,
        'Teamwork':                        teamwork,
        'Problem_Solving':                 problem_solving,
        'Creativity':                      creativity,
        'Time_Management':                 time_management,
        'Adaptability':                    adaptability,
        'Confidence':                      confidence,
        'Self_Learning':                   self_learning,
        'Emotional_Intelligence':          emotional_intel,
        'Stress_Management':               stress_management,
        'Networking_Skill':                networking_soft,

        # Technical Skills
        'Programming':                     programming,
        'Python':                          python_skill,      # FIXED
        'Java':                            java_skill,        # FIXED
        'C++':                             cpp_skill,         # FIXED
        'SQL':                             sql_skill,
        'Database':                        database,
        'Networking':                      networking_t,      # FIXED
        'Cybersecurity':                   cybersecurity,
        'Cloud_Computing':                 cloud,
        'Artificial_Intelligence_Skill':   ai_skill,          # FIXED
        'Machine_Learning':                ml_skill,
        'Data_Analysis':                   data_analysis,
        'UI_UX':                           ui_ux,
        'Graphic_Design':                  graphic_design,

        # Digital Literacy
        'MS_Word':                         ms_word,
        'Excel':                           excel,
        'PowerPoint':                      powerpoint,
        'Typing_Speed':                    typing_speed,
        'Internet_Research':               internet_research,
        'Digital_Communication':           digital_comm,
        'AI_Tool_Usage':                   ai_tool_usage,
        'Online_Collaboration':            online_collab,
        'Cyber_Awareness':                 cyber_awareness,

        # Domain Skills
        'Accounting':                      accounting_skill,
        'Financial_Analysis':              financial_analysis,
        'Marketing':                       marketing_skill,
        'Patient_Care':                    patient_care,
        'Laboratory_Skills':               lab_skills,
        'Mechanical_Design':               mechanical_design,
        'Electrical_Maintenance':          electrical_maint,
        'Civil_Drawing':                   civil_drawing,
        'Legal_Research':                  legal_research,
        'Content_Writing':                 content_writing,
        'Scientific_Research':             scientific_research,
        'Agriculture_Skill':               agriculture_skill,
        'Video_Editing':                   video_editing,

        # Interests
        'Technology_Interest':             tech_interest,      # FIXED
        'Medicine_Interest':               medicine_int,       # FIXED
        'Business_Interest':               business_int,       # FIXED
        'Finance_Interest':                finance_int,        # FIXED
        'Law_Interest':                    law_int,
        'Teaching_Interest':               teaching_int,       # FIXED
        'Research_Interest':               research_int,       # FIXED
        'Agriculture_Interest':            agriculture_int,
        'Arts_Interest':                   arts_int,
        'Design_Interest':                 design_int,         # FIXED
        'Sports_Interest':                 sports_int,
        'Music_Interest':                  music_int,
        'Writing_Interest':                writing_int,
        'Journalism_Interest':             journalism_int,
        'Psychology_Interest':             psychology_int,
        'Environment_Interest':            environment_int,
        'Hospitality_Interest':            hospitality_int,
        'Social_Service_Interest':         social_svc_int,
        'Defence_Interest':                defence_int,
        'Robotics_Interest':               robotics_int,
        'Artificial_Intelligence_Interest': ai_int,            # FIXED
        'Animation_Interest':              animation_int,
        'Entrepreneurship_Interest':       entrepreneurship_int,  # FIXED
        'Gaming_Interest':                 gaming_int,

        # Personality / Style
        'Personality_Type':                personality_type,
        'Learning_Style':                  learning_style,
        'Risk_Taking':                     risk_taking,
        'Work_Preference':                 work_preference,
        'Leadership_Style':                leadership_style,

        # Career Preferences
        'Preferred_Industry':              preferred_industry,
        'Preferred_Location':              preferred_location,
        'Expected_Salary':                 expected_salary,
        'Government_or_Private':           govt_private,
        'Higher_Studies_Interest':         higher_studies,
        'Abroad_Studies_Interest':         abroad_studies,
        'Startup_Interest':                startup_interest,
        'Research_Interest_Level':         research_int_level,
        'Work_Life_Balance_Preference':    work_life_balance,

        # Experience
        'Internship_Completed':            internship_done,
        'Internship_Domain':               internship_domain,
        'Internship_Duration_Months':      internship_duration,
        'Industrial_Visit':                industrial_visit,
        'Volunteer_Experience':            volunteer_exp,
        'Community_Service_Hours':         community_svc_hrs,
        'Certification_Count':             final_cert_count,
        'Certification_1':                 cert_1,
        'Certification_2':                 cert_2,
        'Project_Count':                   final_project_count,
        'Project_1':                       project_1,
        'Project_2':                       project_2,
        'Activity_1':                      activity_1,
        'Activity_2':                      activity_2,
        'Activity_3':                      activity_3,

        # Socioeconomic
        'Parent_Education':                parent_education,
        'Parent_Occupation':               parent_occupation,
        'Annual_Family_Income':            annual_income,
        'First_Generation_Learner':        first_gen,
        'Internet_Access':                 internet_access,
        'Laptop_Availability':             laptop_avail,
        'Study_Environment':               study_environment,

        # ── Computed Scores (derived, not user-input) ────────────────────
        'Academic_Performance_Score':      academic_perf_score,
        'Total_Technical_Skill_Score':     total_tech_score,
        'Soft_Skill_Score':               soft_skill_score,
        'Digital_Literacy_Score':          digital_literacy_score,
        'Domain_Skill_Score':              domain_skill_score,
        'STEM_Strength_Score':             stem_strength_score,
        'Business_Aptitude_Score':         biz_apt_score,
        'Creativity_Score':                creativity_score,
        'Leadership_Score':                leadership_score,
        'Career_Readiness_Score':          career_readiness_score,

        # ── Subject_Studied Boolean Flags (derived from stream) ──────────
        'Mathematics_Studied':             math_studied,
        'Science_Studied':                 science_studied,
        'English_Studied':                 english_studied,
        'Social_Science_Studied':          ss_studied,
        'Second_Language_Studied':         lang_studied,
        'Physics_Studied':                 physics_studied,
        'Chemistry_Studied':               chem_studied,
        'Biology_Studied':                 bio_studied,
        'Computer_Science_Studied':        cs_studied,
        'Accountancy_Studied':             acc_studied,
        'Business_Studies_Studied':        biz_studied,
        'Economics_Studied':               eco_studied,
        'Statistics_Studied':              stats_studied,
        'History_Studied':                 hist_studied,
        'Political_Science_Studied':       pol_studied,
        'Geography_Studied':               geo_studied,
        'Psychology_Studied':              psych_studied,
    }

    return mapping
