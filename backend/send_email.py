# send_message.py
from flask import Blueprint, request, jsonify
from backend.extensions import db
from backend.models import Message  # Make sure this model exists
import requests

send_message_bp = Blueprint('send_message', __name__)

# Replace with your actual secret key from Google reCAPTCHA
RECAPTCHA_SECRET = '6Ld5IGgrAAAAAMwZoJcFYl4pqAxdn4DLMQqhdF0s'

@send_message_bp.route('/send_message', methods=['POST'])
def send_message():
    data = request.form
    recaptcha_response = data.get('g-recaptcha-response')

    if not recaptcha_response:
        return jsonify({'status': 'error', 'message': 'reCAPTCHA not completed.'}), 400

    # Verify reCAPTCHA with Google
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': RECAPTCHA_SECRET,
        'response': recaptcha_response
    }
    response = requests.post(verify_url, data=payload)
    result = response.json()

    if not result.get('success'):
        return jsonify({'status': 'error', 'message': 'reCAPTCHA failed.'}), 400

    # Save message to database
    try:
        message = Message(
            full_name=data.get('full_name'),
            email=data.get('email'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        db.session.add(message)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Message sent successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Failed to save message: {str(e)}'}), 500
