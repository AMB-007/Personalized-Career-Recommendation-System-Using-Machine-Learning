"""
Backend Configuration Module
Configuration and settings for the Flask application
"""

import os
from typing import Dict, Any, Optional

class Config:
    """Base configuration class"""
    # Flask settings
    SECRET_KEY = os.urandom(24)
    SESSION_COOKIE_SECURE = True  # Only send cookie over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent client-side JavaScript from accessing session
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 3600  # Session timeout in seconds (1 hour)

    # Database configuration
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'abc123',  # Will be overridden by environment variable
        'database': 'career_recommendation',
        'pool_name': 'career_pool',
        'pool_size': 5,
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }

    # Model configuration
    MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
    MODEL_PATHS = {
        'xgboost': 'xgboost_model.pkl',
        'label_encoder': 'label_encoder.pkl',
        'feature_columns': 'feature_columns.pkl'
    }

    # App configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')

    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_EXTENSIONS = {'.csv', '.json', '.pkl', '.joblib'}
    UPLOAD_PATH = 'uploads'

    # Log configuration
    LOG_DIR = 'logs'
    LOG_FILE = 'logs/app.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5

    # Prediction configuration
    TOP_N_PREDICTIONS = 5
    PREDICTION_THRESHOLD = 0.0

    # Password configuration
    PASSWORD_HASH_ROUNDS = 12
    PASSWORD_MIN_LENGTH = 8

    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables"""
        config = cls()

        # Override from environment
        if 'DB_PASSWORD' in os.environ:
            config.DB_CONFIG['password'] = os.environ['DB_PASSWORD']

        return config
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DB_CONFIG = {**Config.DB_CONFIG}

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DB_CONFIG = {**Config.DB_CONFIG}

    @classmethod
    def from_env(cls) -> 'ProductionConfig':
        """Create production configuration from environment variables"""
        config = cls()

        if 'DB_PASSWORD' in os.environ:
            config.DB_CONFIG['password'] = os.environ['DB_PASSWORD']

        return config
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DB_CONFIG = {**Config.DB_CONFIG, 'pool_size': 1, 'database': 'career_recommendation_test'}

    @classmethod
    def from_env(cls) -> 'TestingConfig':
        """Create testing configuration from environment variables"""
        config = cls()

        # Use test database
        config.DB_CONFIG['database'] = os.getenv('DB_TEST_NAME', 'career_recommendation_test')

        if 'DB_PASSWORD' in os.environ:
            config.DB_CONFIG['password'] = os.environ['DB_PASSWORD']

        return config

# Configuration factory
def get_config(config_name: Optional[str] = None) -> Config:
    """
    Get configuration based on environment variable

    Args:
        config_name: Configuration name (development, production, testing)

    Returns:
        Config instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development').lower()

    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }

    if config_name not in config_map:
        raise ValueError(f"Unknown configuration: {config_name}")

    return config_map[config_name].from_env()

# Environment variable validation
REQUIRED_ENV_VARS = []

def validate_environment():
    """Validate required environment variables"""
    missing_vars = []
    for var in REQUIRED_ENV_VARS:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# File path utilities
def ensure_directory(path: str):
    """Ensure directory exists"""
    os.makedirs(path, exist_ok=True)

def is_safe_filename(filename: str) -> bool:
    """Check if filename is safe (no path traversal)"""
    return not any(char in filename for char in ['/', '\\', '..', '~'])

def get_file_extension(filename: str) -> str:
    """Get file extension in lowercase"""
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file extension is allowed"""
    return get_file_extension(filename) in allowed_extensions

# Default configuration instance
config = get_config()

# Create necessary directories
os.makedirs(config.LOG_DIR, exist_ok=True)
os.makedirs(config.UPLOAD_PATH, exist_ok=True)