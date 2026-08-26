"""
Admin Control Panel Routes.
Provides administrative monitoring, question management (CRUD), career profile controls,
and system health analytics.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from backend.extensions import db
from backend.models.user import User
from backend.models.student import Student
from backend.models.assessment import AssessmentSession
from backend.models.question import Question, QuestionSection, QuestionOption
from backend.models.career import CareerDomain, Career, CareerSkill, CareerSubject, CareerEducation
from backend.utils.helpers import admin_required, api_response, logger

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    total_students = Student.query.count()
    total_assessments = AssessmentSession.query.count()
    completed_assessments = AssessmentSession.query.filter_by(status='completed').count()
    total_careers = Career.query.count()
    total_questions = Question.query.count()
    domains = CareerDomain.query.all()

    # Recent assessments
    recent_sessions = AssessmentSession.query.order_by(AssessmentSession.created_at.desc()).limit(8).all()

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_assessments=total_assessments,
        completed_assessments=completed_assessments,
        total_careers=total_careers,
        total_questions=total_questions,
        domains=domains,
        recent_sessions=recent_sessions
    )


@admin_bp.route('/questions', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_questions():
    if request.method == 'POST':
        # Create new question
        code = request.form.get('question_code', '').strip()
        text = request.form.get('question_text', '').strip()
        sec_id = int(request.form.get('section_id'))
        q_type = request.form.get('question_type', 'MCQ')
        c_min = int(request.form.get('class_min', 7))
        c_max = int(request.form.get('class_max', 12))
        diff = request.form.get('difficulty', 'Medium')
        skill = request.form.get('skill_category', '').strip()

        if not code or not text:
            flash('Question code and text are required.', 'danger')
            return redirect(url_for('admin.manage_questions'))

        q = Question(
            question_code=code,
            question_text=text,
            section_id=sec_id,
            question_type=q_type,
            class_min=c_min,
            class_max=c_max,
            difficulty=diff,
            skill_category=skill,
            is_active=True
        )
        db.session.add(q)
        db.session.flush()

        # Add sample options if MCQ
        if q_type in ['MCQ', 'SCENARIO']:
            opt1 = request.form.get('option_1', '').strip()
            opt2 = request.form.get('option_2', '').strip()
            opt3 = request.form.get('option_3', '').strip()
            opt4 = request.form.get('option_4', '').strip()
            correct_opt = int(request.form.get('correct_option', 1))

            opts_list = [opt1, opt2, opt3, opt4]
            for idx, opt_text in enumerate(opts_list, 1):
                if opt_text:
                    is_c = (idx == correct_opt)
                    db.session.add(QuestionOption(
                        question_id=q.id,
                        option_text=opt_text,
                        option_value=str(idx),
                        score=1.0 if is_c else 0.0,
                        is_correct=is_c,
                        display_order=idx
                    ))

        db.session.commit()
        logger.info(f"Admin created new question: {code}")
        flash(f'Question {code} successfully created!', 'success')
        return redirect(url_for('admin.manage_questions'))

    # GET: Filter questions
    class_filter = request.args.get('class_level', type=int)
    sec_filter = request.args.get('section_id', type=int)

    query = Question.query
    if class_filter:
        query = query.filter(Question.class_min <= class_filter, Question.class_max >= class_filter)
    if sec_filter:
        query = query.filter(Question.section_id == sec_filter)

    questions = query.order_by(Question.section_id.asc(), Question.display_order.asc()).all()
    sections = QuestionSection.query.order_by(QuestionSection.display_order.asc()).all()

    return render_template(
        'admin/questions.html',
        questions=questions,
        sections=sections,
        class_filter=class_filter,
        sec_filter=sec_filter
    )


@admin_bp.route('/questions/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_question_status(id):
    question = Question.query.get_or_404(id)
    question.is_active = not question.is_active
    db.session.commit()
    logger.info(f"Admin toggled status of question {question.question_code} to {question.is_active}")
    flash(f"Question status updated to {'Active' if question.is_active else 'Inactive'}.", 'info')
    return redirect(url_for('admin.manage_questions'))


@admin_bp.route('/careers', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_careers():
    if request.method == 'POST':
        code = request.form.get('career_code', '').strip()
        name = request.form.get('career_name', '').strip()
        domain_id = int(request.form.get('domain_id'))
        desc = request.form.get('description', '').strip()
        min_edu = request.form.get('minimum_education', '').strip()
        typ_edu = request.form.get('typical_education', '').strip()
        pathway = request.form.get('pathway', '').strip()

        career = Career(
            career_code=code,
            career_name=name,
            domain_id=domain_id,
            description=desc,
            minimum_education=min_edu,
            typical_education=typ_edu,
            career_pathway=pathway,
            is_active=True
        )
        db.session.add(career)
        db.session.commit()
        flash(f'Career profile for {name} created successfully!', 'success')
        return redirect(url_for('admin.manage_careers'))

    careers = Career.query.order_by(Career.domain_id.asc(), Career.career_name.asc()).all()
    domains = CareerDomain.query.all()
    return render_template('admin/careers.html', careers=careers, domains=domains)
