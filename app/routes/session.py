from flask import Flask, request, Response
from app.services.storage import save_file_locally

ALLOWED_EXTENSIONS = {'txt','webm'}

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

    # Check if extension is valid
    if webcam_file and allowed_file(webcam_file.filename) and screen_file and allowed_file(screen_file.filename):
        save_file_locally(webcam_file, '\\sessiontest1')
        save_file_locally(screen_file, '\\sessiontest1')
    else:
        return Response('Error: Files do not follow the extension guidelines', status=400, mimetype='application/json')

    return Response('Create a session', status=201, mimetype='application/json')
