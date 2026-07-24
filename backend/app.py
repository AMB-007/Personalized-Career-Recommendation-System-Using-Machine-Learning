"""
Flask Backend for Personalized Career Recommendation System
Powered by XGBoost Machine Learning Model (82.33% Accuracy)
"""

import os
import re
import json
import logging
import secrets
from datetime import datetime, timedelta
from functools import wraps

import mysql.connector
from mysql.connector import pooling, Error
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash, Response
import bcrypt
import numpy as np

# Import configuration & ML predictor
from config import Config
import predict

# ── Logging setup ──────────────────────────────────────────────────────────
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ── Create Flask app ───────────────────────────────────────────────────────
app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ── Jinja Custom Filters ───────────────────────────────────────────────────
@app.template_filter('substring')
def substring_filter(s, start=0, end=None):
    if not s:
        return ''
    s = str(s)
    if end is None:
        return s[start:]
    try:
        return s[int(start):int(end)]
    except (ValueError, TypeError):
        return s[start:]

# ── Database Connection Pool ───────────────────────────────────────────────
db_config = Config.DB_CONFIG.copy()
try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)
    logger.info("Database connection pool created successfully")
except Error as e:
    logger.error(f"Error creating connection pool: {e}")
    connection_pool = None

# ── Load ML Model via predict module ───────────────────────────────────────
model_loaded = predict.load_model()

# ── Auth & Helper Functions ────────────────────────────────────────────────
def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, "Password is valid"

def get_db_connection():
    if connection_pool is None:
        raise Exception("Database connection pool not available")
    return connection_pool.get_connection()

def execute_query(query, params=None, fetch=False, commit=False):
    conn = None
    try:
        conn = get_db_connection()
        if params is None:
            params = ()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)

        result = None
        if fetch:
            result = cursor.fetchall()
        elif commit:
            conn.commit()
            result = cursor.lastrowid

        cursor.close()
        return result
    except Error as e:
        logger.error(f"Database query error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()

# ── Decorators ─────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Please log in first'}), 401
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin', False):
            if request.is_json:
                return jsonify({'success': False, 'message': 'Admin privileges required'}), 403
            flash('Admin access required.', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ── General Routes ─────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json() if request.is_json else request.form
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    try:
        user_id = session.get('user_id')
        execute_query(
            "INSERT INTO feedback (user_id, subject, message, rating) VALUES (%s, %s, %s, 5)",
            (user_id, f"[{subject}] Contact Form from {name} ({email})", message),
            commit=True
        )
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    except Exception as e:
        logger.error(f"Contact submit error: {e}")
        return jsonify({'success': False, 'message': 'Failed to send message'}), 500

# ── Authentication Routes ──────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return api_login()
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() if request.is_json else request.form
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    user = execute_query(
        "SELECT * FROM users WHERE email = %s AND is_active = TRUE",
        (email,), fetch=True
    )

    if not user or not verify_password(password, user[0]['password_hash']):
        if user:
            execute_query(
                "INSERT INTO login_history (user_id, ip_address, user_agent, success) VALUES (%s, %s, %s, FALSE)",
                (user[0]['user_id'], request.remote_addr, request.headers.get('User-Agent', '')),
                commit=True
            )
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    user_data = user[0]
    execute_query(
        "INSERT INTO login_history (user_id, ip_address, user_agent, success) VALUES (%s, %s, %s, TRUE)",
        (user_data['user_id'], request.remote_addr, request.headers.get('User-Agent', '')),
        commit=True
    )

    session.clear()
    session['user_id'] = user_data['user_id']
    session['email'] = user_data['email']
    session['full_name'] = user_data['full_name']
    session['is_admin'] = bool(user_data.get('is_admin', False))
    session.permanent = True

    return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/dashboard'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return api_register()
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() if request.is_json else request.form
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    age = data.get('age')
    gender = data.get('gender')
    education_level = data.get('education_level', '')
    specialization = data.get('specialization', '').strip()
    cgpa = data.get('cgpa')

    errors = []
    if not full_name or len(full_name) < 2:
        errors.append('Please enter a valid full name')
    if not email or '@' not in email:
        errors.append('Please enter a valid email address')

    is_valid_pwd, pwd_msg = validate_password(password)
    if not is_valid_pwd:
        errors.append(pwd_msg)

    if errors:
        return jsonify({'success': False, 'message': errors[0], 'errors': errors}), 400

    existing_user = execute_query(
        "SELECT user_id FROM users WHERE email = %s",
        (email,), fetch=True
    )

    if existing_user:
        return jsonify({'success': False, 'message': 'Email is already registered'}), 400

    password_hash = hash_password(password)

    try:
        user_id = execute_query(
            """INSERT INTO users
               (full_name, email, password_hash, age, gender, education_level, specialization,
                cgpa, profile_image, is_active, is_admin, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
               """,
            (full_name, email, password_hash,
             int(age) if age else None,
             gender if gender in ['Male', 'Female', 'Other'] else 'Male',
             education_level, specialization,
             float(cgpa) if cgpa else None,
             'default.png'),
            commit=True
        )

        execute_query(
            "INSERT INTO login_history (user_id, ip_address, user_agent, success) VALUES (%s, %s, %s, TRUE)",
            (user_id, request.remote_addr, request.headers.get('User-Agent', '')),
            commit=True
        )

        return jsonify({'success': True, 'message': 'Registration successful', 'user_id': user_id})
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'Database error occurred during registration'}), 500

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ── User Dashboard & Assessment ─────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = execute_query("SELECT * FROM users WHERE user_id = %s", (user_id,), fetch=True)

    recommendations = execute_query(
        """SELECT * FROM prediction_history
           WHERE user_id = %s
           ORDER BY created_at DESC
           LIMIT 5""",
        (user_id,), fetch=True
    )

    history_count = execute_query(
        "SELECT COUNT(*) as count FROM prediction_history WHERE user_id = %s",
        (user_id,), fetch=True
    )

    bookmark_count = execute_query(
        "SELECT COUNT(*) as count FROM bookmarked_careers WHERE user_id = %s",
        (user_id,), fetch=True
    )

    return render_template('dashboard.html',
                          user=user[0] if user else None,
                          recommendations=recommendations or [],
                          history_count=history_count[0]['count'] if history_count else 0,
                          bookmark_count=bookmark_count[0]['count'] if bookmark_count else 0)

@app.route('/assessment', methods=['GET', 'POST'])
@login_required
def assessment():
    if request.method == 'POST':
        return process_assessment()
    return render_template('assessment.html')

@app.route('/api/predict', methods=['POST'])
@login_required
def process_assessment():
    form_data = request.get_json() if request.is_json else request.form.to_dict()
    user_id = session['user_id']

    if not predict.is_loaded():
        predict.load_model()

    try:
        user_features = predict.build_user_input(form_data)
        predictions = predict.predict_careers(user_features, top_n=5)

        top_pick = predictions[0]

        # Save to database
        pred_id = execute_query(
            """INSERT INTO prediction_history
               (user_id, career_name, confidence_score, recommendation_data, created_at)
               VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)""",
            (user_id, top_pick['career'], top_pick['confidence'], json.dumps(predictions)),
            commit=True
        )

        session['last_prediction_id'] = pred_id

        if request.is_json:
            return jsonify({
                'success': True,
                'redirect': f'/recommendation/{pred_id}',
                'predictions': predictions
            })
        return redirect(url_for('view_recommendation', pred_id=pred_id))

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'success': False, 'message': f'Prediction error: {str(e)}'}), 500

# ── Recommendation & Career Details ─────────────────────────────────────────
@app.route('/recommendation')
@app.route('/recommendation/<int:pred_id>')
@login_required
def view_recommendation(pred_id=None):
    user_id = session['user_id']

    if pred_id is None:
        pred_id = session.get('last_prediction_id')

    if pred_id:
        record = execute_query(
            "SELECT * FROM prediction_history WHERE prediction_id = %s AND user_id = %s",
            (pred_id, user_id), fetch=True
        )
    else:
        record = execute_query(
            "SELECT * FROM prediction_history WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
            (user_id,), fetch=True
        )

    if not record:
        flash('No recommendations found. Please complete the assessment first.', 'warning')
        return redirect(url_for('assessment'))

    pred = record[0]
    rec_json = pred.get('recommendation_data')
    if isinstance(rec_json, str):
        predictions = json.loads(rec_json)
    elif isinstance(rec_json, list):
        predictions = rec_json
    else:
        predictions = [{'career': pred['career_name'], 'confidence': float(pred['confidence_score']), 'rank': 1}]

    # Format recommendations array for recommendation.html template
    recommendations_data = []
    for p in predictions:
        c_name = p['career']
        c_detail = execute_query(
            "SELECT * FROM career_details WHERE career_name = %s",
            (c_name,), fetch=True
        )
        detail = c_detail[0] if c_detail else {}
        recommendations_data.append({
            'career_name': c_name,
            'confidence_score': round(p['confidence'], 1),
            'rank': p.get('rank', 1),
            'description': detail.get('description', 'High demand career matching your skill profile and interests.'),
            'average_salary': detail.get('average_salary', '₹6–15 LPA'),
            'demand_level': detail.get('demand_level', 'High'),
            'growth_rate': detail.get('growth_rate', 12.5),
            'required_skills': detail.get('required_skills', 'Problem Solving, Analytical Thinking, Communication'),
            'recommended_certifications': detail.get('recommended_certifications', 'Professional Certification'),
            'career_roadmap': detail.get('career_roadmap', 'Foundational Training → Projects → Entry Role → Senior Role'),
            'future_trends': detail.get('future_trends', 'Strong digital adoption and growth expected over the next decade.')
        })

    top_rec = recommendations_data[0]
    overall_confidence = f"{top_rec['confidence_score']}%"

    return render_template('recommendation.html',
                          recommendations=recommendations_data,
                          overall_confidence=overall_confidence,
                          top_career=top_rec['career_name'],
                          career_description=top_rec['description'],
                          required_skills=top_rec['required_skills'].split(', '),
                          recommended_certifications=top_rec['recommended_certifications'].split(', '),
                          future_trends=top_rec['future_trends'],
                          average_salary=top_rec['average_salary'])

@app.route('/career/<path:career_name>')
def career_detail_page(career_name):
    c_detail = execute_query(
        "SELECT * FROM career_details WHERE career_name = %s",
        (career_name,), fetch=True
    )
    if c_detail:
        detail = c_detail[0]
    else:
        detail = {
            'name': career_name,
            'description': f'Explore opportunities, skills, and industry roadmaps for {career_name}.',
            'avg_salary': '₹6–18 LPA',
            'demand_level': 'High',
            'growth_rate': '15%',
            'icon': 'fas fa-briefcase'
        }
    return render_template('career_details.html', career=detail)

# ── Profile & Feedback ──────────────────────────────────────────────────────
@app.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    user = execute_query("SELECT * FROM users WHERE user_id = %s", (user_id,), fetch=True)
    raw_history = execute_query(
        "SELECT * FROM prediction_history WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,), fetch=True
    )

    formatted_history = []
    if raw_history:
        for row in raw_history:
            item = dict(row)
            if 'confidence_score' in item and item['confidence_score'] is not None:
                try:
                    item['confidence_score'] = float(item['confidence_score'])
                except (ValueError, TypeError):
                    item['confidence_score'] = 0.0
            formatted_history.append(item)

    history_count = len(formatted_history)
    bookmarks_count = execute_query(
        "SELECT COUNT(*) as count FROM bookmarked_careers WHERE user_id = %s",
        (user_id,), fetch=True
    )

    last_pred = formatted_history[0] if formatted_history else None

    return render_template('profile.html',
                          user=user[0] if user else None,
                          history=formatted_history,
                          stats={'total_predictions': history_count, 'bookmarks': bookmarks_count[0]['count'] if bookmarks_count else 0},
                          last_assessment={'communication': 7, 'problem_solving': 8, 'leadership': 7, 'creativity': 8, 'teamwork': 9, 'adaptability': 8, 'confidence': 7, 'critical_thinking': 8} if last_pred else None)

@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    user_id = session['user_id']
    data = request.get_json() if request.is_json else request.form

    full_name = data.get('full_name', '').strip()
    age = data.get('age')
    education_level = data.get('education_level')
    specialization = data.get('specialization', '').strip()
    cgpa = data.get('cgpa')

    try:
        execute_query(
            """UPDATE users SET full_name=%s, age=%s, education_level=%s, specialization=%s, cgpa=%s
               WHERE user_id=%s""",
            (full_name, int(age) if age else None, education_level, specialization, float(cgpa) if cgpa else None, user_id),
            commit=True
        )
        session['full_name'] = full_name
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        return jsonify({'success': False, 'message': 'Failed to update profile'}), 500

@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'POST':
        return submit_feedback()

    user_id = session.get('user_id')
    past_fb = []
    if user_id:
        past_fb = execute_query(
            "SELECT * FROM feedback WHERE user_id = %s ORDER BY created_at DESC LIMIT 5",
            (user_id,), fetch=True
        )
    return render_template('feedback.html', past_feedback=past_fb or [])

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json() if request.is_json else request.form
    user_id = session.get('user_id')
    rating = data.get('rating', 5)
    feedback_type = data.get('feedback_type', 'general')
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'success': False, 'message': 'Feedback message is required'}), 400

    try:
        execute_query(
            "INSERT INTO feedback (user_id, subject, message, rating) VALUES (%s, %s, %s, %s)",
            (user_id, f"Feedback: {feedback_type.title()}", message, int(rating)),
            commit=True
        )
        return jsonify({'success': True, 'message': 'Feedback submitted successfully'})
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        return jsonify({'success': False, 'message': 'Failed to submit feedback'}), 500

# ── Admin Panel ─────────────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        return api_admin_login()
    return render_template('admin_login.html')

@app.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    data = request.get_json() if request.is_json else request.form
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    admin = execute_query("SELECT * FROM admin_users WHERE email = %s", (email,), fetch=True)
    if not admin or not verify_password(password, admin[0]['password_hash']):
        return jsonify({'success': False, 'message': 'Invalid admin credentials'}), 401

    admin_data = admin[0]
    session.clear()
    session['user_id'] = admin_data['admin_id']
    session['admin_name'] = admin_data['full_name']
    session['email'] = admin_data['email']
    session['is_admin'] = True
    session.permanent = True

    return jsonify({'success': True, 'message': 'Admin login successful', 'redirect': '/admin/dashboard'})

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_users = execute_query("SELECT COUNT(*) as count FROM users", fetch=True)[0]['count']
    total_preds = execute_query("SELECT COUNT(*) as count FROM prediction_history", fetch=True)[0]['count']
    total_fb = execute_query("SELECT COUNT(*) as count FROM feedback", fetch=True)[0]['count']

    recent_users = execute_query("SELECT * FROM users ORDER BY created_at DESC LIMIT 5", fetch=True)
    all_users = execute_query(
        """SELECT u.*, COUNT(p.prediction_id) as prediction_count
           FROM users u LEFT JOIN prediction_history p ON u.user_id = p.user_id
           GROUP BY u.user_id ORDER BY u.created_at DESC""",
        fetch=True
    )
    all_predictions_raw = execute_query(
        """SELECT p.*, u.full_name FROM prediction_history p
           JOIN users u ON p.user_id = u.user_id
           ORDER BY p.created_at DESC LIMIT 50""",
        fetch=True
    )
    formatted_all_predictions = []
    if all_predictions_raw:
        for row in all_predictions_raw:
            item = dict(row)
            if 'confidence_score' in item and item['confidence_score'] is not None:
                try:
                    item['confidence_score'] = float(item['confidence_score'])
                except (ValueError, TypeError):
                    item['confidence_score'] = 0.0
            formatted_all_predictions.append(item)

    all_feedback = execute_query(
        """SELECT f.*, u.full_name FROM feedback f
           LEFT JOIN users u ON f.user_id = u.user_id
           ORDER BY f.created_at DESC LIMIT 50""",
        fetch=True
    )

    top_careers = execute_query(
        """SELECT career_name as career, COUNT(*) as count
           FROM prediction_history GROUP BY career_name
           ORDER BY count DESC LIMIT 10""",
        fetch=True
    ) or [{'career': 'Software Engineer', 'count': 12}, {'career': 'Data Scientist', 'count': 9}]

    edu_dist = execute_query(
        """SELECT education_level as level, COUNT(*) as count
           FROM users WHERE education_level IS NOT NULL AND education_level != ''
           GROUP BY education_level""",
        fetch=True
    ) or [{'level': "Bachelor's", 'count': 8}, {'level': "Master's", 'count': 4}]

    return render_template('admin_dashboard.html',
                          now=datetime.now(),
                          stats={'total_users': total_users, 'total_predictions': total_preds, 'total_feedback': total_fb},
                          recent_users=recent_users or [],
                          all_users=all_users or [],
                          all_predictions=formatted_all_predictions,
                          all_feedback=all_feedback or [],
                          top_careers=top_careers,
                          edu_distribution=edu_dist,
                          reg_trend=[{'date': 'Mon', 'count': 3}, {'date': 'Tue', 'count': 5}, {'date': 'Wed', 'count': 8}])

@app.route('/admin/api/delete-user/<int:uid>', methods=['DELETE', 'POST'])
@admin_required
def delete_user(uid):
    try:
        execute_query("DELETE FROM users WHERE user_id = %s", (uid,), commit=True)
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    except Exception as e:
        logger.error(f"Delete user error: {e}")
        return jsonify({'success': False, 'message': 'Failed to delete user'}), 500

@app.route('/admin/export')
@admin_required
def export_admin_report():
    predictions = execute_query(
        "SELECT p.prediction_id, u.full_name, u.email, p.career_name, p.confidence_score, p.created_at FROM prediction_history p JOIN users u ON p.user_id = u.user_id",
        fetch=True
    )
    csv_lines = ["Prediction ID,User Name,Email,Recommended Career,Confidence Score (%),Date"]
    for row in predictions or []:
        csv_lines.append(f'"{row["prediction_id"]}","{row["full_name"]}","{row["email"]}","{row["career_name"]}","{row["confidence_score"]}","{row["created_at"]}"')

    csv_data = "\n".join(csv_lines)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=career_recommendation_report.csv"}
    )

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Admin logged out.', 'info')
    return redirect(url_for('admin_login'))

# ── Bookmarks & Search APIs ────────────────────────────────────────────────
@app.route('/api/careers/search')
def search_careers():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'success': True, 'careers': []})
    careers = execute_query(
        "SELECT career_name, description FROM career_details WHERE career_name LIKE %s LIMIT 10",
        (f"%{query}%",), fetch=True
    )
    return jsonify({'success': True, 'careers': careers or []})

@app.route('/api/bookmark', methods=['POST'])
@login_required
def bookmark_career():
    user_id = session['user_id']
    data = request.get_json() if request.is_json else request.form
    career_name = data.get('career_name', '').strip()

    if not career_name:
        return jsonify({'success': False, 'message': 'Career name required'}), 400

    try:
        execute_query(
            "INSERT INTO bookmarked_careers (user_id, career_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE bookmarked_at=NOW()",
            (user_id, career_name), commit=True
        )
        return jsonify({'success': True, 'message': 'Career bookmarked'})
    except Exception as e:
        logger.error(f"Bookmark error: {e}")
        return jsonify({'success': False, 'message': 'Failed to bookmark'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    import sys
    debug = len(sys.argv) > 1 and sys.argv[1] == 'debug'
    app.run(host='0.0.0.0', port=5000, debug=debug)