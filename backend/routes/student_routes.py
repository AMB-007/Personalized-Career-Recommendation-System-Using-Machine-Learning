"""
Student Profile & Dashboard Routes.
Displays student overview, assessment progress, multi-attempt history, score highlights, and profile settings.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.assessment import AssessmentSession, AssessmentScore
from backend.models.recommendation import CareerRecommendation
from backend.models.student import AcademicScore
from backend.utils.helpers import student_required, api_response, api_error, logger
from backend.utils.validators import validate_academic_score

student_bp = Blueprint('student', __name__)


@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.admin_dashboard'))

    student = current_user.student
    if not student:
        flash('Student profile not found. Please contact support.', 'danger')
        return redirect(url_for('main.index'))

    # Fetch all sessions in reverse chronological order
    all_sessions = AssessmentSession.query.filter_by(student_id=student.id).order_by(AssessmentSession.created_at.desc()).all()
    latest_session = all_sessions[0] if all_sessions else None

    # Build rich attempt history objects with top career recommendation for each completed session
    history_items = []
    for idx, sess in enumerate(reversed(all_sessions), 1):
        top_rec = None
        score_obj = None
        if sess.status == 'completed':
            top_rec = CareerRecommendation.query.filter_by(assessment_id=sess.id, rank_position=1).first()
            score_obj = AssessmentScore.query.filter_by(assessment_id=sess.id).first()
        history_items.append({
            'attempt_number': idx,
            'session': sess,
            'top_rec': top_rec,
            'score_obj': score_obj
        })
    history_items.reverse()  # Most recent attempt on top

    recent_scores = None
    recent_recs = []
    if latest_session and latest_session.status == 'completed':
        recent_scores = AssessmentScore.query.filter_by(assessment_id=latest_session.id).first()
        recent_recs = CareerRecommendation.query.filter_by(assessment_id=latest_session.id).order_by(CareerRecommendation.rank_position.asc()).limit(3).all()

    return render_template(
        'dashboard.html',
        student=student,
        latest_session=latest_session,
        all_sessions=all_sessions,
        history_items=history_items,
        recent_scores=recent_scores,
        recent_recs=recent_recs
    )


@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    student = current_user.student
    if not student:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        student.first_name = request.form.get('first_name', student.first_name).strip()
        student.last_name = request.form.get('last_name', student.last_name).strip()
        student.board = request.form.get('board', student.board).strip()
        student.medium = request.form.get('medium', student.medium).strip()

        # Update stream if Grade 11/12
        if student.class_level in [11, 12]:
            student.stream = request.form.get('stream', student.stream).strip()

        # Update academic scores
        ac = student.academic_scores or AcademicScore(student_id=student.id)
        ac.mathematics_score = float(request.form.get('math_score', ac.mathematics_score or 0)) if request.form.get('math_score') else ac.mathematics_score
        ac.science_score = float(request.form.get('science_score', ac.science_score or 0)) if request.form.get('science_score') else ac.science_score
        ac.computer_science_score = float(request.form.get('cs_score', ac.computer_science_score or 0)) if request.form.get('cs_score') else ac.computer_science_score
        ac.english_score = float(request.form.get('english_score', ac.english_score or 0)) if request.form.get('english_score') else ac.english_score

        if not student.academic_scores:
            db.session.add(ac)

        db.session.commit()
        flash('Profile and academic records updated successfully!', 'success')
        return redirect(url_for('student.profile_page'))

    return render_template('profile.html', student=student, academic=student.academic_scores)


# ------------------------------------------------------------
# JSON REST API Endpoints
# ------------------------------------------------------------

@student_bp.route('/api/student/profile', methods=['GET'])
@login_required
def api_get_profile():
    if not current_user.student:
        return api_error("Student profile not found.", status_code=404)
    return api_response(current_user.student.to_dict())


@student_bp.route('/api/student/profile', methods=['PUT'])
@login_required
def api_update_profile():
    student = current_user.student
    if not student:
        return api_error("Student profile not found.", status_code=404)

    data = request.get_json() or {}
    if 'first_name' in data:
        student.first_name = data['first_name']
    if 'last_name' in data:
        student.last_name = data['last_name']
    if 'class_level' in data:
        student.class_level = int(data['class_level'])
    if 'stream' in data:
        student.stream = data['stream']
    if 'board' in data:
        student.board = data['board']

    db.session.commit()
    return api_response(student.to_dict())
