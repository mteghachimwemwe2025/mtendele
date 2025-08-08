import os
from flask import Blueprint, request, render_template, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
from backend.models import Testimony
from backend.extensions import db

testimony_bp = Blueprint('testimony_bp', __name__)

@testimony_bp.route('/submit_testimony', methods=['GET', 'POST'])
def submit_testimony():
    if request.method == 'POST':
        email = request.form['email']
        description = request.form['description']
        image_file = request.files.get('image')

        image_filename = None
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            upload_folder = os.path.join(current_app.instance_path, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
            image_filename = filename  # Only save the filename to DB

        new_testimony = Testimony(
            email=email,
            description=description,
            image=image_filename,  # Save only filename
            time=datetime.now().time(),
            date=datetime.now().date(),
            approve=None
        )

        db.session.add(new_testimony)
        db.session.commit()

        return "Testimony submitted successfully and awaiting approval."

    return render_template('submit_testmonies.html')
