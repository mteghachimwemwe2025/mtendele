# backend/delete_edit_ministries.py

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from backend.models import db, Ministry
import os
from datetime import datetime

manage_ministries_bp = Blueprint('manage_ministries', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@manage_ministries_bp.route('/delete_edit_ministries', methods=['POST'])
def update_ministry():
    ministry_id = request.form.get('id')
    ministry_name = request.form.get('ministry_name')
    description = request.form.get('description')
    meeting_time = request.form.get('meeting_time')
    meeting_days = request.form.get('meeting_days')
    image = request.files.get('image')

    if not ministry_id:
        return jsonify({'success': False, 'message': 'Missing ministry ID'})

    ministry = Ministry.query.get(ministry_id)
    if not ministry:
        return jsonify({'success': False, 'message': 'Ministry not found'})

    ministry.ministry_name = ministry_name
    ministry.description = description
    ministry.meeting_time = meeting_time
    ministry.meeting_days = meeting_days

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        unique_filename = f"{int(datetime.now().timestamp())}_{filename}"
        upload_folder_path = os.path.join(current_app.root_path, 'static/uploads')
        os.makedirs(upload_folder_path, exist_ok=True)
        image_path = os.path.join(upload_folder_path, unique_filename)
        image.save(image_path)
        ministry.image_path = f"/static/uploads/{unique_filename}"

    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@manage_ministries_bp.route('/delete_ministry', methods=['GET'])
def delete_ministry():
    ministry_id = request.args.get('id')
    if not ministry_id:
        return jsonify({'success': False, 'message': 'Missing ID'})
    ministry = Ministry.query.get(ministry_id)
    if not ministry:
        return jsonify({'success': False, 'message': 'Ministry not found'})

    try:
        db.session.delete(ministry)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@manage_ministries_bp.route('/fetch_ministries', methods=['GET'])
def fetch_ministries():
    ministries = Ministry.query.order_by(Ministry.ministry_name.asc()).all()
    result = []
    for m in ministries:
        result.append({
            'id': m.id,
            'name': m.ministry_name,
            'description': m.description,
            'time': m.meeting_time,
            'days': m.meeting_days,
            'image_path': m.image_path or '/static/uploads/placeholder.png'
        })
    return jsonify(result)
