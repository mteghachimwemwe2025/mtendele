# fetch_categories.py
from flask import Blueprint, jsonify
from backend.extensions import db
from backend.models import Category  # Assuming you have a Category model

fetch_categories_bp = Blueprint('fetch_categories', __name__)

@fetch_categories_bp.route('/fetch_categories')
def fetch_categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])
