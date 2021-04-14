from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return Response('Welcome to EyeLab', status=418, mimetype='application/json')

@app.route('/api/user/sessions')
def get_user_sessions():
    # Pass userid as parameter on the route so we can query by user
    print('REQUEST', request.args.__getitem__('userid'))
    return Response('User sessions', status=200, mimetype='application/json')

@app.route('/api/session', methods=['GET','POST','PATCH','DELETE'])
def session():
    if request.method == 'GET':
        return Response('Return a session by id passed on params', status=200, mimetype='application/json')
    elif request.method == 'POST':
        return Response('Create a session', status=201, mimetype='application/json')
    elif request.method == 'DELETE':
        return Response('Delete a session', status=200, mimetype='application/json')
    elif request.method == 'PATCH':
        return Response('Update a session', status=200, mimetype='application/json')
    return 'Invalid request method'
