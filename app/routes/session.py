from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from pathlib import Path
import os

ALLOWED_EXTENSIONS = {'txt','webm'}
UPLOAD_FOLDER = f'{Path().absolute()}\\resources'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_session():
    if 'webcamfile' not in request.files or 'screenfile' not in request.files:
        return Response('Error: Files not found on the request', status=400, mimetype='application/json')

    webcam_file = request.files['webcamfile']
    screen_file = request.files['screenfile']

    if webcam_file and allowed_file(webcam_file.filename) and screen_file and allowed_file(screen_file.filename):
        webcam_filename = secure_filename(webcam_file.filename)
        screen_filename = secure_filename(screen_file.filename)
            
        webcam_file.save(os.path.join(app.config['UPLOAD_FOLDER'], webcam_filename))
        screen_file.save(os.path.join(app.config['UPLOAD_FOLDER'], screen_filename))
    else:
        return Response('Error: Files do not follow the extension guidelines', status=400, mimetype='application/json')

    return Response('Create a session', status=201, mimetype='application/json')
