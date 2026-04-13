from flask import Blueprint, jsonify
from backend.extensions import db
from backend.models import Testimony

get_approved_bp = Blueprint('get_approved_bp', __name__)

@get_approved_bp.route('/get_approved_testmonies', methods=['GET'])
def get_approved_testmonies():
    testimonies = (
        Testimony.query
        .filter_by(approve='yes')
        .order_by(Testimony.date.desc(), Testimony.time.desc())
        .all()
    )

    result = []
    for t in testimonies:
        result.append({
            'email': t.email,
            'description': t.description,
            'image': t.image,
            'date': t.date.strftime('%Y-%m-%d'),
            'time': t.time.strftime('%H:%M:%S')
        })

    return jsonify(result)
