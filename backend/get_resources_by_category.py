# backend/get_resources_by_category.py

from flask import Blueprint, jsonify, request
from backend.extensions import db
from backend.models import Resource
from datetime import datetime

get_resources_by_category_bp = Blueprint('get_resources_by_category_bp', __name__)

@get_resources_by_category_bp.route('/get_resources_by_category', methods=['GET'])
def get_resources_by_category():
    try:
        category_id = request.args.get('category_id', type=int)

        if category_id is None:
            return jsonify({'error': 'Missing category_id parameter'}), 400

        # Fetch resources from the database based on category_id
        resources = Resource.query.filter_by(category_id=category_id).order_by(Resource.date.desc()).all()

        resource_list = []
        for res in resources:
            resource_list.append({
                'id': res.id,
                'title': res.title,
                'description': res.description,
                'file': res.file,  # Ensure this is a complete or relative URL
                'date': res.date.strftime('%Y-%m-%d') if res.date else None
            })

        return jsonify(resource_list)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
