from flask import Flask, request, Response
from app.services.storage import save_file_locally
from app.models.session import Session
from app.services import database as db
import time
import json

ALLOWED_EXTENSIONS = {'txt', 'webm'}
COLLECTION_NAME = u'session'

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_session():
    # Get files from request
    if 'webcamfile' not in request.files or 'screenfile' not in request.files:
        return Response('Error: Files not found on the request', status=400, mimetype='application/json')

    webcam_file = request.files['webcamfile']
    screen_file = request.files['screenfile']
    title = request.form['title']
    description = request.form['description']
    website_url = request.form['website_url']
    user_id = request.form['user_id']
    timestamp = time.time()
    session_id = f'\\{timestamp}{title}'

    # Check if extension is valid
    if webcam_file and allowed_file(webcam_file.filename) and screen_file and allowed_file(screen_file.filename):
        webcam_url = save_file_locally(webcam_file, session_id)
        screen_url = save_file_locally(screen_file, session_id)
    else:
        return Response('Error: Files do not follow the extension guidelines', status=400, mimetype='application/json')

    # Save session on database
    session = Session(
        id=session_id,
        title=title, 
        description=description, 
        user_id=user_id, 
        created_date=timestamp, 
        website_url=website_url, 
        screen_record_url=screen_url, 
        webcam_record_url=webcam_url, 
        heatmap_url='', 
        callib_url=''
    )
    
    db.create_document(COLLECTION_NAME, session_id, session.to_dict())

    return Response('Session Created!', status=201, mimetype='application/json')

def get_user_sessions():
    user_id = request.args.__getitem__('user_id')
    field = u'user_id' 
    op = u'=='
    docs =  db.get_documents(COLLECTION_NAME, field, op, user_id)
    sessions = []
    for doc in docs:
        sessions.append(
            doc.to_dict()
        )
    return Response(json.dumps(sessions), status=200, mimetype='application/json')

def get_session_by_id():
    session_id = request.args.__getitem__('id')
    doc = db.get_document(COLLECTION_NAME, doc_id=session_id)
    
    if doc.exists:
        session = doc.to_dict()
        return Response(json.dumps(session), status=200, mimetype='application/json')
    else:
        return Response('Session does not exist', status=404, mimetype='application/json')
