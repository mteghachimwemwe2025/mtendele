# backend/view_new_series.py
from flask import Blueprint, jsonify, request
from backend.extensions import db
from backend.models import Series, Sermon
import os

view_new_series_bp = Blueprint('view_new_series', __name__)

@view_new_series_bp.route('/view_new_series')
def get_series():
    series_id = request.args.get('series_id', type=int)

    if not series_id:
        series_list = Series.query.order_by(Series.id.desc()).with_entities(Series.id, Series.title).all()
        return jsonify({'series_list': [{'id': s.id, 'title': s.title} for s in series_list]})

    series = Series.query.filter_by(id=series_id).first()
    if not series:
        return jsonify({'error': 'Series not found.'})

    # ✅ Properly build the URL to match /uploads/<filename>
    image_path = f"/uploads/{os.path.basename(series.image)}" if series.image else ''

    sermons = Sermon.query.filter_by(series_id=series_id).all()
    sermon_data = []
    for s in sermons:
        media_path = s.media if s.media and s.media.startswith("uploads/") else f"uploads/{s.media.lstrip('/')}" if s.media else ''
        notes_path = s.notes if s.notes and s.notes.startswith("uploads/") else f"uploads/{s.notes.lstrip('/')}" if s.notes else ''
        sermon_data.append({
            'title': s.title,
            'speaker': s.speaker,
            'date': s.date,
            'scripture': s.scripture,
            'description': s.description,
            'media': media_path,
            'notes': notes_path,
            'youtube_url': s.youtube_url
        })

    return jsonify({
        'series': {
            'title': series.title,
            'description': series.description,
            'image': image_path
        },
        'sermons': sermon_data
    })
