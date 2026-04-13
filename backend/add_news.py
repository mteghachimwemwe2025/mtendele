# backend/add_news.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from backend.models import db, News, Category
import os
from datetime import datetime

add_news_bp = Blueprint('add_news', __name__)

UPLOAD_FOLDER = 'instance/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@add_news_bp.route('/add_news_handle', methods=['GET'])
def show_add_news():
    return render_template('add_news_handle.html')


@add_news_bp.route('/fetch_categories', methods=['GET'])
def fetch_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])


@add_news_bp.route('/fetch_news', methods=['GET'])
def fetch_news():
    news = News.query.order_by(News.date_posted.desc()).all()
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'content': n.content,
        'image_path': n.image_path,
        'date_posted': n.date_posted.strftime('%Y-%m-%d'),
        'category_id': n.category_id
    } for n in news])


@add_news_bp.route('/fetch_single_news', methods=['GET'])
def fetch_single_news():
    news_id = request.args.get('id')
    news = News.query.get(news_id)
    if not news:
        return jsonify({'error': 'News not found'}), 404
    return jsonify({
        'id': news.id,
        'title': news.title,
        'content': news.content,
        'category_id': news.category_id
    })


@add_news_bp.route('/add_news_handler', methods=['POST'])
def add_news_handler():
    title = request.form.get('title')
    content = request.form.get('content')
    category_id = request.form.get('category_id')
    image = request.files.get('image')

    if not all([title, content, category_id]):
        return redirect(url_for('add_news.show_add_news'))

    image_path = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        unique_filename = f"{int(datetime.now().timestamp())}_{filename}"
        upload_folder_path = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(upload_folder_path, exist_ok=True)
        image.save(os.path.join(upload_folder_path, unique_filename))
        # ✅ This path is stored in DB for use in browser
        image_path = f"/uploads/{unique_filename}"

    new_news = News(
        title=title,
        content=content,
        image_path=image_path,
        category_id=category_id,
        date_posted=datetime.utcnow()
    )
    db.session.add(new_news)
    db.session.commit()
    return redirect(url_for('add_news.show_add_news'))


@add_news_bp.route('/delete_news', methods=['GET'])
def delete_news():
    news_id = request.args.get('id')
    news = News.query.get(news_id)
    if news:
        db.session.delete(news)
        db.session.commit()
        return "success"
    return "News not found", 404


@add_news_bp.route('/update_news', methods=['POST'])
def update_news():
    news_id = request.form.get('id')
    title = request.form.get('title')
    content = request.form.get('content')
    category_id = request.form.get('category_id')
    image = request.files.get('image')

    if not all([news_id, title, content, category_id]):
        return "All fields are required", 400

    news = News.query.get(news_id)
    if not news:
        return "News not found", 404

    news.title = title
    news.content = content
    news.category_id = category_id

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        unique_filename = f"{int(datetime.now().timestamp())}_{filename}"
        upload_folder_path = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(upload_folder_path, exist_ok=True)
        image.save(os.path.join(upload_folder_path, unique_filename))
        news.image_path = f"/uploads/{unique_filename}"  # ✅ Correct public path

    db.session.commit()
    return "success"
