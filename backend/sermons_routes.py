from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from backend.extensions import db
from backend.models import Sermon
import os

sermon_bp = Blueprint('sermon_bp', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'ogg', 'webm', 'm4a'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@sermon_bp.route('/get_sermons', methods=['GET'])
def get_sermons():
    sermons = Sermon.query.order_by(Sermon.date.desc()).all()
    return jsonify([sermon.to_dict() for sermon in sermons])

@sermon_bp.route('/add_sermon', methods=['POST'])
def add_sermon():
    title = request.form.get('title')
    speaker = request.form.get('speaker')
    date = request.form.get('date')
    scripture = request.form.get('scripture')
    description = request.form.get('description')
    notes = request.form.get('notes')
    image = request.form.get('image')
    youtube_url = request.form.get('youtube_url', "N/A")  # default to "N/A" if not provided

    if 'media' not in request.files:
        return jsonify({"status": "error", "message": "Media file is required"}), 400

    file = request.files['media']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        new_sermon = Sermon(
            title=title,
            speaker=speaker,
            date=date,
            scripture=scripture,
            description=description,
            media=file_path,
            notes=notes,
            image=image,
            youtube_url=youtube_url if youtube_url else "N/A"
        )
        db.session.add(new_sermon)
        db.session.commit()
        return jsonify({"status": "success", "media_path": file_path})
    return jsonify({"status": "error", "message": "Invalid media file"}), 400

@sermon_bp.route('/update_sermon', methods=['POST'])
def update_sermon():
    id = request.form.get('id')
    sermon = Sermon.query.get(id)
    if not sermon:
        return jsonify({"status": "error", "message": "Sermon not found"}), 404

    sermon.title = request.form.get('title')
    sermon.speaker = request.form.get('speaker')
    sermon.date = request.form.get('date')
    sermon.scripture = request.form.get('scripture')
    sermon.description = request.form.get('description')
    sermon.notes = request.form.get('notes')
    sermon.image = request.form.get('image')
    
    youtube_url = request.form.get('youtube_url')
    if youtube_url:
        sermon.youtube_url = youtube_url
    else:
        sermon.youtube_url = sermon.youtube_url or "N/A"

    file = request.files.get('media')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        sermon.media = file_path

    db.session.commit()
    return jsonify({"status": "success"})

@sermon_bp.route('/delete_sermon', methods=['POST'])
def delete_sermon():
    data = request.get_json()
    sermon = Sermon.query.get(data.get('id'))
    if not sermon:
        return jsonify({"status": "error", "message": "Sermon not found"}), 404

    db.session.delete(sermon)
    db.session.commit()
    return jsonify({"status": "deleted"})
