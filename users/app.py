from flask import request, make_response, jsonify
from config import createApp
from tokens import loginRequired
from db import getUser, addUser, loginUser

app = createApp()

jsonResponse = lambda data, code: make_response(jsonify(data), code)

#--------------------------------------------------------------
# Rutas:

@app.route('/users/')
@loginRequired(get_username=True)
def getUserInfo(username):
    
    response = getUser(username)
    
    return jsonResponse(response['data'], response['code'])

@app.route('/users/', methods=['POST'])
def createUser():
    
    username = request.json.get('username')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    age = request.json.get('age')

    error_response = {}

    if not username:
        error_response['username'] = 'This field is required'
    if not password:
        error_response['password'] = 'This field is required'
    if not first_name:
        error_response['first_name'] = 'This field is required'
    if not last_name:
        error_response['last_name'] = 'This field is required'
    if not age:
        error_response['age'] = 'This field is required'

    if error_response:
        return jsonResponse(error_response, 400)
    
    response = addUser(username, password, first_name, last_name, age)
    
    return jsonResponse(response['data'], response['code'])

@app.route('/users/login/', methods=['POST'])
def login():

    username = request.json.get('username')
    password = request.json.get('password')
    
    error_response = {}

    if not username:
        error_response['username'] = 'This field is required'
    if not password:
        error_response['password'] = 'This field is required'
    
    if error_response:
        return jsonResponse(error_response, 400)
    
    response = loginUser(username, password)
    
    return jsonResponse(response['data'], response['code'])

#--------------------------------------------------------------

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
