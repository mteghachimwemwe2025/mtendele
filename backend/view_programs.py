from flask import Blueprint, jsonify
from backend.models import Program, Activity
from datetime import datetime

view_programs_bp = Blueprint('view_programs', __name__)

@view_programs_bp.route('/load_program_list', methods=['GET'])
def load_programs():
    programs = Program.query.order_by(Program.name.asc()).all()
    return jsonify({
        'status': 'success',
        'programs': [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'image_path': p.image_path,
                'date_posted': None  # Placeholder for compatibility
            } for p in programs
        ]
    })

@view_programs_bp.route('/load_activity_full', methods=['GET'])
def load_activities():
    activities = Activity.query.order_by(Activity.date_posted.desc()).all()
    return jsonify({
        'status': 'success',
        'activities': [
            {
                'id': a.id,
                'title': a.title,
                'content': a.content,
                'image_path': a.image_path,
                'date_posted': a.date_posted.strftime('%Y-%m-%d') if a.date_posted else None,
                'program_name': a.program.name if a.program else '',
                'is_recent': (datetime.utcnow() - a.date_posted).days <= 3 if a.date_posted else False
            } for a in activities
        ]
    })
