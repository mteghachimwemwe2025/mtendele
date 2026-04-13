import os
import traceback
from flask import Blueprint, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

from backend.models import db, Sermon

# ✅ ALLOW INSECURE TRANSPORT FOR LOCAL TESTING
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

youtube_bp = Blueprint('youtube_bp', __name__, url_prefix='')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'uploads'))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secret.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

@youtube_bp.route("/authorize_youtube/<int:sermon_id>")
def authorize(sermon_id):
    if not os.path.exists(CLIENT_SECRETS_FILE):
        return f"❌ ERROR: client_secret.json not found at {CLIENT_SECRETS_FILE}"

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('youtube_bp.oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    session['sermon_id'] = sermon_id
    return redirect(authorization_url)

@youtube_bp.route("/oauth2callback")
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('youtube_bp.oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    session['credentials'] = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }
    return redirect(url_for('youtube_bp.upload_to_youtube'))

@youtube_bp.route("/upload_to_youtube")
def upload_to_youtube():
    if 'credentials' not in session or 'sermon_id' not in session:
        return redirect(url_for('youtube_bp.authorize', sermon_id=session.get('sermon_id', 0)))

    creds = Credentials(**session['credentials'])

    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            session['credentials'] = {
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes
            }
        except Exception as e:
            return f"❌ Failed to refresh credentials: {e}"

    youtube = build("youtube", "v3", credentials=creds)

    sermon = Sermon.query.get(session['sermon_id'])
    if not sermon:
        return "❌ Sermon not found."

    filename = sermon.media
    if not filename:
        return "❌ Sermon media filename is empty or missing."

    if filename.startswith("uploads/") or filename.startswith("uploads\\"):
        filename = filename.split('/', 1)[-1] if '/' in filename else filename.split('\\', 1)[-1]

    video_path = os.path.join(UPLOADS_DIR, filename)
    print("🎬 Looking for video at:", video_path)

    if not os.path.exists(video_path):
        return f"❌ Video file not found: {video_path}"

    file_size = os.path.getsize(video_path)
    print(f"📁 File size: {file_size} bytes")

    mime_type = "video/mp4"

    body = {
        'snippet': {
            'title': sermon.title or 'Mtendele Sermon Upload',
            'description': 'Uploaded using Flask + YouTube API',
            'tags': ['sermon', 'church', 'mtendele'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'unlisted'
        }
    }

    media = MediaFileUpload(video_path, mimetype=mime_type, chunksize=5 * 1024 * 1024, resumable=True)

    try:
        upload_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = upload_request.next_chunk()
            if status:
                print(f"Uploading... {int(status.progress() * 100)}%")

        video_url = f"https://www.youtube.com/watch?v={response['id']}"

        sermon.youtube_url = video_url
        db.session.commit()

        return f"✅ Successfully uploaded video: <a href='{video_url}' target='_blank'>{video_url}</a>"

    except HttpError as e:
        err_content = e.content.decode() if hasattr(e, 'content') else str(e)
        tb = traceback.format_exc()
        print("❌ HttpError during upload:\n", tb)
        return f"❌ Upload failed with HTTP error: {err_content}<br><pre>{tb}</pre>"

    except Exception as e:
        tb = traceback.format_exc()
        print("❌ Upload failed with exception:\n", tb)
        return f"❌ Upload failed: {str(e)}<br><pre>{tb}</pre>"
