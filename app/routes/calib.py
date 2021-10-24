from flask import Flask, request, Response
from app.services.storage import save_file_locally
from app.eye_tracker import callibrator

ALLOWED_EXTENSIONS = {'txt', 'webm'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_calib():
    if 'webcamfile' not in request.files:
        return Response('Error: File not found on the request', status=400, mimetype='application/json')
    
    webcam_file = request.files['webcamfile']
    user_id = request.form['user_id']
    mouse_events = request.form['mouse_events']

    if webcam_file and allowed_file(webcam_file.filename):
        webcam_url = save_file_locally(webcam_file, f'calib-{user_id}')
    else:
        return Response('Error: Files do not follow the extension guidelines', status=400, mimetype='application/json')

    callibrator.start_calib(mouse_events, webcam_url)
    
    Response('System calibrated', status=200)