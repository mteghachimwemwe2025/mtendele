# backend/add_program.py
from flask import Blueprint, request, jsonify, current_app
from backend.models import db, Program
import os
from werkzeug.utils import secure_filename
from datetime import datetime

program_bp = Blueprint('add_program', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@program_bp.route('/add_program_handler', methods=['POST'])
def add_program():
    name = request.form.get('name')
    description = request.form.get('description')
    image = request.files.get('image')

    if not name or not description:
        return "Program name and description are required", 400

    if Program.query.filter_by(name=name).first():
        return "Program already exists", 400

    image_path = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        unique_filename = f"{int(datetime.now().timestamp())}_{filename}"
        upload_folder_path = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(upload_folder_path, exist_ok=True)
        image.save(os.path.join(upload_folder_path, unique_filename))
        image_path = f"/uploads/{unique_filename}"

    new_program = Program(name=name, description=description, image_path=image_path)
    db.session.add(new_program)
    db.session.commit()

    return "Program added successfully"

@program_bp.route('/get_programs', methods=['GET'])
def get_programs():
    programs = Program.query.order_by(Program.id.desc()).all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'image_path': p.image_path  # This is already in the correct format (e.g., /uploads/xxx.jpg)
        } for p in programs
    ])

@program_bp.route('/delete_program', methods=['POST'])
def delete_program():
    program_id = request.form.get('id')
    if not program_id:
        return "Missing program ID", 400

    program = Program.query.get(program_id)
    if not program:
        return "Program not found", 404

    if program.image_path:
        full_path = os.path.join(current_app.instance_path, program.image_path.strip('/\\'))
        if os.path.exists(full_path):
            os.remove(full_path)

    db.session.delete(program)
    db.session.commit()
    return "Program deleted successfully"

@program_bp.route('/update_programs', methods=['POST'])
def update_program():
    program_id = request.form.get('program_id')
    name = request.form.get('name')
    description = request.form.get('description')
    image = request.files.get('image')

    if not all([program_id, name, description]):
        return "All fields are required.", 400

    program = Program.query.get(program_id)
    if not program:
        return "Program not found", 404

    duplicate = Program.query.filter(Program.name == name, Program.id != program.id).first()
    if duplicate:
        return "Program name already in use.", 400

    program.name = name
    program.description = description

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        unique_filename = f"{int(datetime.now().timestamp())}_{filename}"
        upload_folder_path = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(upload_folder_path, exist_ok=True)
        image_path = os.path.join(upload_folder_path, unique_filename)
        image.save(image_path)

        # Delete old image
        if program.image_path:
            old_path = os.path.join(current_app.instance_path, program.image_path.strip('/\\'))
            if os.path.exists(old_path):
                os.remove(old_path)

        # Save browser-friendly path
        program.image_path = f"/uploads/{unique_filename}"

    db.session.commit()
    return "Program updated successfully"
