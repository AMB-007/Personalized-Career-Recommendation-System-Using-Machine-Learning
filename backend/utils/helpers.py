"""
Helper utilities, decorators, structured logging, and standard response formatters.
"""

import logging
from functools import wraps
from flask import jsonify, session, request, redirect, url_for, flash
from flask_login import current_user

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s (%(funcName)s): %(message)s'
)
logger = logging.getLogger('career_guidance_app')


def admin_required(f):
    """Decorator to enforce Admin role access control."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required', 'code': 'UNAUTHORIZED'}), 401
            flash('Please log in as an administrator to access this area.', 'warning')
            return redirect(url_for('auth.login_page'))

        if current_user.role != 'admin':
            logger.warning(f"Unauthorized admin access attempt by User ID {current_user.id} ({current_user.username})")
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Administrative privileges required', 'code': 'FORBIDDEN'}), 403
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('student.dashboard'))

        return f(*args, **kwargs)
    return decorated_function


def student_required(f):
    """Decorator to enforce Student role access control."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required', 'code': 'UNAUTHORIZED'}), 401
            return redirect(url_for('auth.login_page'))

        if current_user.role != 'student' or not current_user.student:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Student profile required', 'code': 'FORBIDDEN'}), 403
            return redirect(url_for('admin.admin_dashboard'))

        return f(*args, **kwargs)
    return decorated_function


def api_response(data=None, message="Success", status_code=200, meta=None):
    """Standardized JSON API response structure."""
    payload = {
        'success': 200 <= status_code < 300,
        'message': message,
        'data': data
    }
    if meta is not None:
        payload['meta'] = meta
    return jsonify(payload), status_code


def api_error(message="An error occurred", status_code=400, errors=None, code="BAD_REQUEST"):
    """Standardized JSON API error response."""
    payload = {
        'success': False,
        'error': message,
        'code': code
    }
    if errors:
        payload['details'] = errors
    return jsonify(payload), status_code
