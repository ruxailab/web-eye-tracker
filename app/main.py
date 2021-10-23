from flask import Flask, request, Response
from flask_cors import CORS
from app.routes import session as session_route

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
    
    return 'Invalid request method for route'

@app.route('/api/session', methods=['GET','POST','PATCH','DELETE'])
def session():
    # Get by ID
    if request.method == 'GET':
        return Response('Return a session by id passed on params', status=200, mimetype='application/json')
    
    # Create Session
    elif request.method == 'POST':
        return session_route.create_session()

    # Delete by ID
    elif request.method == 'DELETE':
        return Response('Delete a session', status=200, mimetype='application/json')
    
    # Update by ID
    elif request.method == 'PATCH':
        return Response('Update a session', status=200, mimetype='application/json')
    
    return 'Invalid request method for route'

@app.route('/api/session/results/heatmap', methods=['GET'])
def manage_heatmap():
    if request.method == 'GET':
        # TO DO: Generate heatmap
        return Response('Generated heatmap', status=200, mymetype='application/json')
    return 'Invalid request method for route'

@app.route('/api/calibrate', methods=['POST'])
def calibrate():
    if request.method == 'POST':
        # TO DO: Do system calibration
        return Response('System calibrated', status=200, mymetype='application/json')
    return 'Invalid request method for route'