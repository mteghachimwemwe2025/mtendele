from flask import Blueprint, jsonify, request, current_app, send_from_directory
from backend.models import Testimony
from backend.extensions import db
from datetime import datetime
import os

approve_bp = Blueprint('approve_bp', __name__)

# Serve uploaded testimony images
@approve_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(current_app.instance_path, 'uploads')
    return send_from_directory(upload_folder, filename)

# Get testimonies pending approval
@approve_bp.route('/get_testimonies', methods=['GET'])
def get_testimonies():
    pending = Testimony.query.filter_by(approve=None).all()
    result = []
    for t in pending:
        result.append({
            'id': t.id,
            'email': t.email,
            'description': t.description,
            'image': f"uploads/{t.image}" if t.image else None,
            'date': t.date.isoformat() if t.date else None
        })
    return jsonify(result)

# Get approved testimonies for display
@approve_bp.route('/approved_testimonies', methods=['GET'])
def get_approved_testimonies():
    approved = Testimony.query.filter_by(approve='yes').order_by(Testimony.date.desc()).all()
    result = []
    for t in approved:
        result.append({
            'id': t.id,
            'email': t.email,
            'description': t.description,
            'image': f"uploads/{t.image}" if t.image else None,
            'date': t.date.isoformat() if t.date else None
        })
    return jsonify(result)

# Approve or reject a testimony (admin function)
@approve_bp.route('/approve_testimony', methods=['POST'])
def approve_testimony():
    data = request.get_json()
    testimony_id = data.get('id')
    approval = data.get('approve')

    testimony = Testimony.query.get(testimony_id)
    if not testimony:
        return jsonify({'error': 'Testimony not found'}), 404

    if approval in ['yes', 'no']:
        testimony.approve = approval
        testimony.approval_date = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': f'Testimony {approval}d successfully'})
    else:
        return jsonify({'error': 'Invalid approval value'}), 400