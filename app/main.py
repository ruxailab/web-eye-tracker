from flask import Flask, request, Response
from flask_cors import CORS
from app.routes import session as session_route
from app.routes import calib as calib_route

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def welcome():
    return Response(f'Welcome to EyeLab!', status=200, mimetype='application/json')

@app.route('/api/user/sessions', methods=['GET'])
def get_user_sessions():
    # Get user sessions
    if request.method == 'GET':
        return session_route.get_user_sessions()
    
    return Response('Invalid request method for route', status=405, mimetype='application/json')

@app.route('/api/session', methods=['GET','POST','PATCH','DELETE'])
def session():
    # Get by ID
    if request.method == 'GET':
        return session_route.get_session_by_id()
    
    # Create Session
    elif request.method == 'POST':
        return session_route.create_session()

    # Delete by ID
    elif request.method == 'DELETE':
        return session_route.delete_session_by_id()
    
    # Update by ID
    elif request.method == 'PATCH':
        return session_route.update_session_by_id()
    
    return Response('Invalid request method for route', status=405, mimetype='application/json')

@app.route('/api/session/results/heatmap', methods=['GET'])
def manage_heatmap():
    if request.method == 'GET':
        # TO DO: Generate heatmap
        return Response('Generated heatmap', status=200, mymetype='application/json')
    return Response('Invalid request method for route', status=405, mimetype='application/json')

@app.route('/api/calibrate', methods=['POST'])
def calibrate():
    if request.method == 'POST':
        # Do system calibration
        return calib_route.save_calib()
    return Response('Invalid request method for route', status=405, mimetype='application/json')