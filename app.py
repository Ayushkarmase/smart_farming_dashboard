import os
from flask import Flask, redirect, url_for, session
from config import Config
from database.db_init import init_db

# Blueprints
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.fertilizer import fertilizer_bp
from blueprints.forecasting import forecasting_bp
from blueprints.news import news_bp
from blueprints.admin import admin_bp
from blueprints.history import history_bp
from blueprints.info import info_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLite database and default seed records
    init_db()

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(fertilizer_bp)
    app.register_blueprint(forecasting_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(info_bp)

    @app.context_processor
    def inject_user_context():
        return {
            'current_user': {
                'id': session.get('user_id'),
                'name': session.get('user_name', 'Guest'),
                'email': session.get('user_email', ''),
                'role': session.get('user_role', 'user')
            }
        }

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"================================================================")
    print(f" Fritz-Haber Agritech: Smart Farming Dashboard is running!")
    print(f" Access URL: http://127.0.0.1:{port}")
    print(f" Demo Farmer: farmer@agritech.com | Password: Farmer@123")
    print(f" Demo Admin:  admin@agritech.com  | Password: Admin@123")
    print(f"================================================================")
    app.run(host='0.0.0.0', port=port, debug=True)
