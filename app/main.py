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

@app.route('/api/session/results/record', methods=['GET'])
def manage_recording():
    if request.method == 'GET':
        return session_route.session_results_record()
    return Response('Invalid request method for route', status=405, mimetype='application/json')

@app.route('/api/session/results', methods=['GET'])
def manage_results():
    if request.method == 'GET':
        return session_route.session_results()
    return Response('Invalid request method for route', status=405, mimetype='application/json')
