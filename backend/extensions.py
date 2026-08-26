from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
