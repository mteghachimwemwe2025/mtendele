# backend/resource_routes.py
import os
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
from backend.extensions import db
from backend.models import Resource, ResourceCategory

resource_bp = Blueprint('resource_bp', __name__)

UPLOAD_FOLDER = 'uploads/resources/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# GET route to render the upload page
@resource_bp.route('/resource_routes', methods=['GET'])
def resource_routes_get():
    return render_template('manage_resource.html')  # Your HTML template filename here

# POST route to handle form submission
@resource_bp.route('/resource_routes', methods=['POST'])
def resource_routes():
    title = request.form['title']
    description = request.form.get('description', '')
    category_id = int(request.form['category_id'])
    file = request.files['file']
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower()

    allowed = ['pdf', 'mp3', 'docx', 'zip', 'pptx', 'xlsx']
    if ext not in allowed:
        return "Invalid file type", 400

    file_path = os.path.join(UPLOAD_FOLDER, f"{int(datetime.now().timestamp())}_{filename}")
    file.save(file_path)

    resource = Resource(
        title=title,
        description=description,
        category_id=category_id,
        file=file_path,
        date=datetime.now().date()
    )
    db.session.add(resource)
    db.session.commit()
    return redirect('/resource_routes')

# Route to fetch all categories
@resource_bp.route('/get_categories')
def get_categories():
    categories = ResourceCategory.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])

# Route to fetch all resources
@resource_bp.route('/get_all_resources')
def get_all_resources():
    resources = Resource.query.order_by(Resource.date.desc()).all()

    def get_file_type(filename):
        ext = filename.split('.')[-1].lower()
        if ext in ['mp3', 'wav', 'aac']: return 'audio'
        if ext in ['mp4', 'webm', 'avi']: return 'video'
        if ext in ['pdf', 'doc', 'docx', 'zip']: return 'document'
        return 'other'

    return jsonify([
        {
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file': r.file,
            'file_type': get_file_type(r.file),
            'date': r.date.strftime('%Y-%m-%d'),
            'category_id': r.category_id
        } for r in resources
    ])

# Route to fetch resources by category
@resource_bp.route('/get_resources_by_category')
def get_resources_by_category():
    category_id = request.args.get('category_id')
    if not category_id:
        return jsonify([])

    resources = Resource.query.filter_by(category_id=category_id).order_by(Resource.date.desc()).all()

    return jsonify([
        {
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file': r.file,
            'date': r.date.strftime('%Y-%m-%d') if r.date else '',
            'category_id': r.category_id
        } for r in resources
    ])

# ✅ New route to fetch recent (latest) resources for default landing
@resource_bp.route('/get_recent_resources')
def get_recent_resources():
    recent = Resource.query.order_by(Resource.date.desc()).limit(5).all()
    return jsonify([
        {
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file': r.file,
            'date': r.date.strftime('%Y-%m-%d') if r.date else '',
            'category_id': r.category_id
        } for r in recent
    ])

# Edit resource
@resource_bp.route('/edit_resource', methods=['POST'])
def edit_resource():
    id = request.form.get('id')
    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category_id')

    resource = Resource.query.get(id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404

    resource.title = title
    resource.description = description
    resource.category_id = category_id

    file = request.files.get('file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, f"{int(datetime.now().timestamp())}_{filename}")
        file.save(path)
        if os.path.exists(resource.file):
            os.remove(resource.file)
        resource.file = path

    db.session.commit()
    return jsonify({"message": "Resource updated successfully"})

# Delete resource
@resource_bp.route('/delete_resource', methods=['POST'])
def delete_resource():
    data = request.get_json()
    id = data.get('id')
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404

    if os.path.exists(resource.file):
        os.remove(resource.file)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted"})
