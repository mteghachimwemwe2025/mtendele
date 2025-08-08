# backend/get_all_sermons.py
from flask import Blueprint, jsonify
from backend.models import Sermon
from backend.extensions import db

get_all_sermons_bp = Blueprint('get_all_sermons_bp', __name__)

@get_all_sermons_bp.route('/get_all_sermons')
def get_all_sermons():
    try:
        sermons = Sermon.query.order_by(Sermon.date.desc()).all()
        result = []
        for s in sermons:
            result.append({
                'id': s.id,
                'title': s.title,
                'speaker': s.speaker,
                'date': s.date.strftime("%Y-%m-%d") if s.date else '',
                'scripture': s.scripture,
                'description': s.description,
                'media': s.media if s.media else '',
                'notes': s.notes if s.notes else '',
                'image': s.image if s.image else ''
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
