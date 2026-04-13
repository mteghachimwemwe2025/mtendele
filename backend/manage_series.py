from flask import Blueprint, request, jsonify, current_app
from backend.extensions import db
from backend.models import Series, Sermon
from werkzeug.utils import secure_filename
import os
import json

series_bp = Blueprint('series_bp', __name__)
UPLOAD_FOLDER = os.path.join('instance', 'uploads')

@series_bp.route('/get_series', methods=['GET'])
def get_series():
    series_list = Series.query.all()
    data = []
    for s in series_list:
        sermons = Sermon.query.filter_by(series_id=s.id).with_entities(Sermon.id, Sermon.title).all()
        data.append({
            'id': s.id,
            'title': s.title,
            'description': s.description,
            'image': s.image,
            'sermon_count': len(sermons),
            'sermons': [{'id': ser.id, 'title': ser.title} for ser in sermons]
        })
    return jsonify(data)

@series_bp.route('/add_series', methods=['POST'])
def add_series():
    title = request.form.get('title')
    description = request.form.get('description')
    sermons = json.loads(request.form.get('sermons', '[]'))

    image = request.files.get('image')
    image_path = ''
    if image:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

    new_series = Series(title=title, description=description, image=image_path)
    db.session.add(new_series)
    db.session.commit()

    for sermon_id in sermons:
        sermon = Sermon.query.get(sermon_id)
        if sermon:
            sermon.series_id = new_series.id
    db.session.commit()

    return jsonify({"status": "success"})

@series_bp.route('/update_series', methods=['POST'])
def update_series():
    id = request.form.get('id')
    series = Series.query.get(id)
    if not series:
        return jsonify({"status": "error", "message": "Series not found"}), 404

    title = request.form.get('title')
    description = request.form.get('description')
    sermons = json.loads(request.form.get('sermons', '[]'))

    image = request.files.get('image')
    if image:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
        series.image = image_path

    series.title = title
    series.description = description
    db.session.commit()

    current_sermons = Sermon.query.filter_by(series_id=series.id).all()
    current_ids = set(s.id for s in current_sermons)
    new_ids = set(sermons)

    for s_id in current_ids - new_ids:
        sermon = Sermon.query.get(s_id)
        if sermon:
            sermon.series_id = None

    for s_id in new_ids:
        sermon = Sermon.query.get(s_id)
        if sermon:
            sermon.series_id = series.id

    db.session.commit()
    return jsonify({"status": "updated"})

@series_bp.route('/delete_series', methods=['POST'])
def delete_series():
    data = request.get_json()
    id = data.get('id')
    series = Series.query.get(id)
    if not series:
        return jsonify({"status": "error", "message": "Series not found"}), 404

    for sermon in Sermon.query.filter_by(series_id=series.id).all():
        sermon.series_id = None

    db.session.delete(series)
    db.session.commit()
    return jsonify({"status": "deleted"})
