import os
import tempfile

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def is_serverless():
    return bool(
        os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or 
        os.environ.get('NETLIFY') or 
        os.environ.get('VERCEL')
    )

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'agritech-smart-farming-secret-key-2024')
    if is_serverless():
        DATABASE = os.path.join(tempfile.gettempdir(), 'agritech.db')
        UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'uploads')
    else:
        DATABASE = os.path.join(BASE_DIR, 'database', 'agritech.db')
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    DEBUG = not is_serverless()

