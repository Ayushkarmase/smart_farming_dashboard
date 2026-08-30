import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'agritech-smart-farming-secret-key-2024')
    DATABASE = os.path.join(BASE_DIR, 'database', 'agritech.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    DEBUG = True
