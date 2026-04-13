# routes/message_api.py

from flask import Blueprint, request, jsonify
from backend.models import db, Message
from datetime import datetime

message_bp = Blueprint('message_bp', __name__)

@message_bp.route('/view_email', methods=['GET', 'POST'])
def handle_messages():
    action = request.args.get('action')
    
    if action == 'get_messages':
        return get_messages()
    elif action == 'mark_as_read':
        return mark_as_read()
    elif action == 'delete_messages':
        return delete_messages()
    else:
        return jsonify({"success": False, "error": "Invalid action"})

def get_messages():
    try:
        messages = Message.query.order_by(Message.created_at.desc()).all()
        message_list = []
        for msg in messages:
            status = msg.status or 'unread'
            message_list.append({
                'id': msg.id,
                'full_name': msg.full_name,
                'email': msg.email,
                'subject': msg.subject,
                'message': msg.message,
                'status': status,
                'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return jsonify({"success": True, "messages": message_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def mark_as_read():
    try:
        data = request.get_json()
        message_ids = data.get('messageIds', [])
        if not message_ids:
            return jsonify({"success": False, "error": "No message IDs provided"})

        Message.query.filter(Message.id.in_(message_ids)).update({'status': 'read'}, synchronize_session='fetch')
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def delete_messages():
    try:
        data = request.get_json()
        message_ids = data.get('messageIds', [])
        if not message_ids:
            return jsonify({"success": False, "error": "No message IDs provided"})

        Message.query.filter(Message.id.in_(message_ids)).delete(synchronize_session='fetch')
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
