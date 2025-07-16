import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "secret_key")

    # MongoDB setup
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    mongo_db_name = os.getenv("MONGO_DB_NAME", "Seraphis_db")
    mongo_client = MongoClient(mongo_uri)
    app.mongo_db = mongo_client[mongo_db_name]

    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.appointment import appointment_bp
    from app.routes.ai import ai_bp
    from app.routes.admin import admin_bp
    from app.routes.doctor import doctor_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    # Example route
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)