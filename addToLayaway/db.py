from werkzeug.local import LocalProxy
from pymongo import MongoClient
from flask import current_app
import time

#==================================================================

def getDB():
    
    URI = current_app.config['MONGO_URI']
    
    while True:
        try:
            client = MongoClient(URI)
            break
        except :
            print('Log: Trying to connect to the database...')
            time.sleep(2)

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

#==================================================================

def addUser(username, collLayaway):

    collUsers = db.Users

    user_id = collUsers.find_one({'username': username}).get('id')

    user = {
        'user_id': user_id,
        'username': username,
        'layaway': []
    }

    collLayaway.insert_one(user)

    return user

def addComic(username, comic):
    
    collLayaway = db.Layaway

    user = collLayaway.find_one({'username': username})
    
    if not user:
        user = addUser(username, collLayaway)

    if comic in user.get('layaway'):
        return {
            'data': {'message': 'The Comic is already exists in registry'},
            'code': 400
        }
    
    collLayaway.update_one({'username': username}, {'$push': {'layaway': comic}})

    response = {
        'data': {
            'message': 'Comic added successfully',
            'comic': comic
        },
        'code': 200
    }

    return response
