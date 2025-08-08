# backend/logout.py

from flask import Blueprint, redirect, url_for, flash
from flask_login import logout_user, login_required

logout_bp = Blueprint('logout_bp', __name__, url_prefix='/logout')

@logout_bp.route('/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login_bp.login'))  # Adjust 'auth.login' if your login route has a different endpoint
