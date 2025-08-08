# load_news_full.py
from flask import Blueprint, request, jsonify
from backend.extensions import db
from backend.models import News, Category  # Assuming you have a News and Category model
from sqlalchemy.orm import joinedload

load_news_bp = Blueprint('load_news', __name__)

@load_news_bp.route('/load_news_full')
def load_news():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 3))
    category = request.args.get('category', '')

    query = db.session.query(News).options(joinedload(News.category)).order_by(News.date_posted.desc())
    if category:
        query = query.join(Category).filter(Category.name == category)

    news_items = query.offset(offset).limit(limit).all()

    news_list = []
    for item in news_items:
        news_list.append({
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'image_path': item.image_path,
            'date_posted': item.date_posted.strftime('%Y-%m-%d'),
            'category_name': item.category.name if item.category else 'Uncategorized',
        })

    return jsonify({'status': 'success', 'news': news_list})
