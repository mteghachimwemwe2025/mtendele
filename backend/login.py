from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from backend.models import User
from flask_bcrypt import Bcrypt

login_bp = Blueprint('login_bp', __name__)
bcrypt = Bcrypt()

# Hardcoded credentials
users = {
    '4444': {'password': 'admin', 'role': 'admin'},
    '5555': {'password': 'student', 'role': 'student'}
}

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        reg_number = request.form['reg_number'].strip()
        password = request.form['password'].strip()

        # First check hardcoded credentials
        if reg_number in users and users[reg_number]['password'] == password:
            role = users[reg_number]['role']
            user = User(reg_number=reg_number, password=password, email=f"{reg_number}@test.com", role=role)
            login_user(user)

            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif role == 'student':
                return redirect(url_for('student_dashboard'))

        else:
            # Check database users
            user = User.query.filter_by(reg_number=reg_number).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user.role == 'student':
                    return redirect(url_for('student_dashboard'))
                else:
                    return redirect(url_for('index'))
            else:
                flash("Invalid credentials")

    return render_template('login.html')
