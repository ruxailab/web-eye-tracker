from flask import Flask, request, Response

from app.eye_tracker import main as eye_tracker
from app.routes import session as session_route

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    a = eye_tracker.setup()
    return Response(f'Welcome to EyeLab {a}', status=418, mimetype='application/json')

@app.route('/api/user/sessions')
def get_user_sessions():
    # Pass userid as parameter on the route so we can query by user
    print('REQUEST', request.args.__getitem__('userid'))
    return Response('User sessions', status=200, mimetype='application/json')

@app.route('/api/session', methods=['GET','POST','PATCH','DELETE'])
def session():
    if request.method == 'GET':
        return Response('Return a session by id passed on params', status=200, mimetype='application/json')
    
    # Create Session
    elif request.method == 'POST':
       return session_route.create_session()

    elif request.method == 'DELETE':
        return Response('Delete a session', status=200, mimetype='application/json')
    elif request.method == 'PATCH':
        return Response('Update a session', status=200, mimetype='application/json')
    return 'Invalid request method'
