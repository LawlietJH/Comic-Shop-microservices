from werkzeug.local import LocalProxy
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import current_app
from jwt import encode as jwt_encode, decode as jwt_decode
from jwt import exceptions as jwt_exceptions
import os

#==================================================================

def getDB():
    
    URI = current_app.config['MONGO_URI']
    client = MongoClient(URI)

    return client.ComicShop

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(getDB)

#==================================================================

def getToken(username=None, token=None):

    collTokens = db.Tokens

    token = collTokens.find_one(
        {'token': token} if token
        else {'username': username}
    )

    return token

def createToken(data: dict):
    token = jwt_encode(
        payload={**data, 'exp': datetime.now()+timedelta(7)},
        key=os.getenv('JWTSECRET'),
        algorithm='HS256'
    )
    return token.decode('UTF-8')

def validateToken(token):
    try:
        jwt_decode(token, key=os.getenv('JWTSECRET'), algorithm='HS256')
        return {'code': 200}
    except jwt_exceptions.DecodeError:
        return {'data': {'message': 'Invalid Token'}, 'code': 401}
    except jwt_exceptions.ExpiredSignatureError:
        collTokens = db.Tokens
        collTokens.delete_one({'token': token})
        return {'data': {'message': 'Token Expired'}, 'code': 401}

#==================================================================

# def getUsers():
#     collUsers = db.Users
#     data = collUsers.find()
#     return data 

def getUser(username):
    
    collUsers = db.Users
    
    user = collUsers.find_one({'username': username})

    if not user:
        return {'data': {'message': 'Not found'}, 'code': 404}

    return {'data': user, 'code': 200}

def addUser(username, password, first_name, last_name, age):
    
    collUsers = db.Users

    dup_user = collUsers.find_one({'username': username})

    if dup_user:
        return {
            'data': {'mesage': f'Username {repr(username)} already exists'},
            'code': 409
        }

    user = {
        'data': {
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'age': age
        },
        'code': 201
    }

    collUsers.insert_one(user['data'])
    
    return user

def loginUser(username, password):

    collUsers = db.Users
    collTokens = db.Tokens

    user = collUsers.find_one({'username': username})

    if not user or not user.get('password') == password:
        return {
            'data': {'mesage': f'The username or password are incorrect'},
            'code': 409
        }

    expired = None
    token_doc = getToken(username)

    if token_doc:

        token = token_doc.get('token')
        resp = validateToken(token)
        
        if resp['code'] == 401:
            expired = resp['data']['message'] == 'Token Expired'

    if not token_doc or expired:
        token = createToken({
            'username': username
        })
        collTokens.insert_one({
            'id_user': user.get('_id'),
            'username': username,
            'token': token
        })
    
    fullname = user.get('first_name') + ' ' + user.get('last_name')
    response = {
        'data': {
            'id': user.get('_id'),
            'name': fullname,
            'age': user.get('age'),
            'token': token
        },
        'code': 200
    }

    return response
