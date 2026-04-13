# backend/add_category.py
from flask import Blueprint, request, jsonify, render_template
from backend.models import db, Category

add_category_bp = Blueprint('add_category', __name__)

@add_category_bp.route('/add_category_uploader', methods=['GET'])
def show_add_category_page():
    return render_template('add_category_uploader.html')


@add_category_bp.route('/add_category_handler', methods=['POST'])
def add_category():
    name = request.form.get('name', '').strip()
    if not name:
        return "Category name is required"

    # Check if category exists
    existing = Category.query.filter_by(name=name).first()
    if existing:
        return "Category already exists"

    # Add new category
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return "Category added successfully"


@add_category_bp.route('/delete_category', methods=['POST'])
def delete_category():
    id = request.form.get('id')
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return "Category deleted successfully"
    return "Error deleting category"


@add_category_bp.route('/update_category', methods=['POST'])
def update_category():
    category_id = request.form.get('category_id')
    name = request.form.get('name', '').strip()

    if not category_id or not name:
        return "Invalid category or name"

    existing = Category.query.filter(Category.name == name, Category.id != category_id).first()
    if existing:
        return "Category name already in use"

    category = Category.query.get(category_id)
    if category:
        category.name = name
        db.session.commit()
        return "Category updated successfully"
    return "Error updating category"


@add_category_bp.route('/get_categories', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    category_list = [{'id': c.id, 'name': c.name} for c in categories]
    return jsonify(category_list)
