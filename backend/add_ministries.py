from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from backend.models import db, Ministry

add_ministries_bp = Blueprint('add_ministries', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@add_ministries_bp.route('/add-ministry', methods=['GET', 'POST'])
def add_ministry():
    if request.method == 'POST':
        ministry_name = request.form.get('ministry_name')
        description = request.form.get('description')
        meeting_time = request.form.get('meeting_time')
        meeting_days = request.form.get('meeting_days')
        image = request.files.get('image')

        # Validate required fields
        if not all([ministry_name, description, meeting_time, meeting_days]):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for('add_ministries.add_ministry'))

        image_path = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            unique_filename = f"{int(datetime.now().timestamp())}_{filename}"
            upload_folder_path = os.path.join(current_app.instance_path, 'uploads')
            os.makedirs(upload_folder_path, exist_ok=True)
            image.save(os.path.join(upload_folder_path, unique_filename))
            image_path = f"/uploads/{unique_filename}"
        else:
            flash("Valid image is required (png, jpg, jpeg, gif).", "danger")
            return redirect(url_for('add_ministries.add_ministry'))

        new_ministry = Ministry(
            ministry_name=ministry_name,
            description=description,
            image_path=image_path,
            meeting_time=meeting_time,
            meeting_days=meeting_days
        )

        try:
            db.session.add(new_ministry)
            db.session.commit()
            flash("Ministry added successfully!", "success")
            return redirect(url_for('add_ministries.add_ministry'))
        except Exception as e:
            db.session.rollback()
            flash(f"Database error: {str(e)}", "danger")

    return render_template('add_ministries_handle.html')
