from flask import Flask, send_from_directory
import pymysql
import os
from dotenv import load_dotenv  # NEW: for local .env use

from backend.config import Config
from backend.extensions import db, login_manager

# Ensure pymysql works as MySQLdb
pymysql.install_as_MySQLdb()

# Load environment variables from .env (for local development)
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Load configuration
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import User model for user_loader callback
from backend.models import User

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Import models after db initialized
from backend import models

# Import routes
import backend.routes

# Setup Google API credentials (for YouTube upload)
from google_auth_oauthlib.flow import Flow

# Ensure client_secret.json exists
if not os.path.exists('client_secret.json'):
    print("❌ client_secret.json not found! Make sure it's downloaded and placed in your project root.")

# Register blueprints
from backend.login import login_bp
from backend.logout import logout_bp
from backend.add_category import add_category_bp
from backend.add_news import add_news_bp
from backend.fetch_categories import fetch_categories_bp
from backend.load_news_full import load_news_bp
from backend.add_program import program_bp
from backend.add_activity import activity_bp
from backend.view_programs import view_programs_bp
from backend.send_email import send_message_bp
from backend.view_message import message_bp
from backend.sermons_routes import sermon_bp
from backend.youtube_uploader import youtube_bp
from backend.manage_series import series_bp
from backend.resource_category import resource_category_bp
from backend.resource_routes import resource_bp
from backend.view_new_series import view_new_series_bp
from backend.get_all_sermons import get_all_sermons_bp
from backend.get_resources_by_category import get_resources_by_category_bp
from backend.add_ministries import add_ministries_bp
from backend.delete_edit_ministries import manage_ministries_bp
from backend.testimony_routes import testimony_bp
from backend.approve import approve_bp
from backend.get_approved_testmonies import get_approved_bp


app.register_blueprint(get_approved_bp)
app.register_blueprint(approve_bp)
app.register_blueprint(testimony_bp)
app.register_blueprint(manage_ministries_bp)
app.register_blueprint(add_ministries_bp)
app.register_blueprint(get_resources_by_category_bp)
app.register_blueprint(get_all_sermons_bp)
app.register_blueprint(view_new_series_bp)
app.register_blueprint(resource_bp)
app.register_blueprint(resource_category_bp)
app.register_blueprint(series_bp)
app.register_blueprint(youtube_bp)
app.register_blueprint(sermon_bp)
app.register_blueprint(message_bp)
app.register_blueprint(send_message_bp)
app.register_blueprint(view_programs_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(program_bp)
app.register_blueprint(fetch_categories_bp)
app.register_blueprint(load_news_bp)
app.register_blueprint(add_news_bp)
app.register_blueprint(add_category_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)

# ✅ Serve uploaded files from either /uploads or instance/uploads
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    # First check: project root /uploads
    root_uploads = os.path.abspath(os.path.join(os.path.dirname(__file__), '../uploads'))
    root_file_path = os.path.join(root_uploads, filename)

    # Second check: instance/uploads
    instance_uploads = os.path.join(app.instance_path, 'uploads')
    instance_file_path = os.path.join(instance_uploads, filename)

    if os.path.exists(root_file_path):
        return send_from_directory(root_uploads, filename)
    elif os.path.exists(instance_file_path):
        return send_from_directory(instance_uploads, filename)
    else:
        return "File not found", 404

# Create tables on startup
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

# Run the app locally
if __name__ == '__main__':
    app.run(debug=True)
