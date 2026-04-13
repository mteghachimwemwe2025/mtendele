# backend/activity_routes.py
from flask import Blueprint, request, jsonify, redirect, url_for, current_app, send_from_directory
from backend.models import db, Activity, Program
import os
from werkzeug.utils import secure_filename
from datetime import datetime

activity_bp = Blueprint('activity', __name__)

UPLOAD_FOLDER = 'uploads'  # Will be served as /uploads/<filename>
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@activity_bp.route('/add_activity_handler', methods=['POST'])
def add_activity():
    title = request.form.get('title')
    content = request.form.get('content')
    program_id = request.form.get('program_id')
    image = request.files.get('image')

    if not title or not content or not program_id:
        return "All fields are required", 400

    image_path = None
    if image and allowed_file(image.filename):
        filename = secure_filename(f"{int(datetime.now().timestamp())}_{image.filename}")
        upload_folder_path = os.path.join(current_app.instance_path, UPLOAD_FOLDER)
        os.makedirs(upload_folder_path, exist_ok=True)
        image.save(os.path.join(upload_folder_path, filename))
        image_path = f"/uploads/{filename}"

    new_activity = Activity(
        title=title,
        content=content,
        program_id=program_id,
        image_path=image_path,
        date_posted=datetime.utcnow()
    )
    db.session.add(new_activity)
    db.session.commit()
    return "Activity added successfully"


@activity_bp.route('/get_programs', methods=['GET'])
def get_programs():
    programs = Program.query.order_by(Program.name.asc()).all()
    return jsonify([{'id': p.id, 'name': p.name} for p in programs])


@activity_bp.route('/get_activities', methods=['GET'])
def get_activities():
    activities = db.session.query(Activity, Program).join(Program).order_by(Activity.date_posted.desc()).all()
    return jsonify([
        {
            'id': a.id,
            'title': a.title,
            'content': a.content,
            'program_name': p.name,
            'image_path': a.image_path,
            'date_posted': a.date_posted.strftime('%Y-%m-%d') if a.date_posted else ''
        }
        for a, p in activities
    ])


@activity_bp.route('/get_single_activity', methods=['GET'])
def get_single_activity():
    activity_id = request.args.get('id')
    if not activity_id:
        return jsonify({'message': 'Missing ID'}), 400

    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'message': 'Activity not found'}), 404

    return jsonify({
        'id': activity.id,
        'title': activity.title,
        'content': activity.content,
        'program_id': activity.program_id
    })


@activity_bp.route('/delete_activity', methods=['GET'])
def delete_activity():
    activity_id = request.args.get('id')
    if not activity_id:
        return "Missing activity ID", 400

    activity = Activity.query.get(activity_id)
    if not activity:
        return "Activity not found", 404

    # Delete image if exists
    if activity.image_path:
        image_file_path = os.path.join(current_app.instance_path, activity.image_path.strip("/").replace("/", os.sep))
        if os.path.exists(image_file_path):
            os.remove(image_file_path)

    db.session.delete(activity)
    db.session.commit()
    return "Activity deleted successfully"


@activity_bp.route('/update_activity', methods=['POST'])
def update_activity():
    activity_id = request.form.get('id')
    title = request.form.get('title')
    content = request.form.get('content')
    program_id = request.form.get('program_id')
    image = request.files.get('image')

    if not all([activity_id, title, content, program_id]):
        return "All fields are required", 400

    activity = Activity.query.get(activity_id)
    if not activity:
        return "Activity not found", 404

    activity.title = title
    activity.content = content
    activity.program_id = program_id

    if image and allowed_file(image.filename):
        filename = secure_filename(f"{int(datetime.now().timestamp())}_{image.filename}")
        upload_folder_path = os.path.join(current_app.instance_path, UPLOAD_FOLDER)
        os.makedirs(upload_folder_path, exist_ok=True)
        new_image_path = os.path.join(upload_folder_path, filename)
        image.save(new_image_path)

        # Delete old image
        if activity.image_path:
            old_path = os.path.join(current_app.instance_path, activity.image_path.strip("/").replace("/", os.sep))
            if os.path.exists(old_path):
                os.remove(old_path)

        activity.image_path = f"/uploads/{filename}"

    db.session.commit()
    return "Activity updated successfully"


# Serve uploaded image files
@activity_bp.route('/uploads/<filename>')
def serve_uploaded_image(filename):
    return send_from_directory(os.path.join(current_app.instance_path, UPLOAD_FOLDER), filename)
