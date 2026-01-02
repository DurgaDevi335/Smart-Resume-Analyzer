import os

class Config:
    # Basic Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ats-scanner-secret-key-9988'
    
    # Database Configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'resume_data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB Upload Limit
    
    # Model Paths
    MODEL_PATH = os.path.join(BASE_DIR, 'models/ats_model.pkl')
    VECTORIZER_PATH = os.path.join(BASE_DIR, 'models/vectorizer.pkl')