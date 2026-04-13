from flask import Blueprint, request, jsonify
from backend.extensions import db
from backend.models import ResourceCategory, Resource

resource_category_bp = Blueprint('resource_category', __name__)

@resource_category_bp.route('/add_category', methods=['POST'])
def add_category():
    data = request.form
    name = data.get('categoryName', '').strip()
    if not name:
        return "Category name cannot be empty.", 400

    new_category = ResourceCategory(name=name)
    db.session.add(new_category)
    db.session.commit()
    return "Category added successfully.", 200


@resource_category_bp.route('/get_categories', methods=['GET'])
def get_categories():
    categories = ResourceCategory.query.with_entities(ResourceCategory.id, ResourceCategory.name).all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])


@resource_category_bp.route('/update_category', methods=['POST'])
def update_category():
    data = request.get_json()
    cat_id = data.get('id')
    new_name = data.get('name', '').strip()

    if not cat_id or not new_name:
        return "Invalid request.", 400

    category = ResourceCategory.query.get(cat_id)
    if not category:
        return "Category not found.", 404

    category.name = new_name
    db.session.commit()
    return "Category updated successfully.", 200


@resource_category_bp.route('/delete_category', methods=['POST'])
def delete_category():
    data = request.get_json()
    cat_id = data.get('id')

    if not cat_id:
        return "Invalid request.", 400

    category = ResourceCategory.query.get(cat_id)
    if not category:
        return "Category not found.", 404

    # Delete resources under this category first
    Resource.query.filter_by(category_id=cat_id).delete()

    db.session.delete(category)
    db.session.commit()
    return "Category and its resources deleted successfully.", 200
