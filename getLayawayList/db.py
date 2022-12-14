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

def getComicList(username, filter=None):
    
    collLayaway = db.Layaway

    user = collLayaway.find_one({'username': username})
    
    if not user:
        return {
            'data': {'message': "You don't have layaway comics"},
            'code': 200
        }

    layaway = user.get('layaway')

    def sortKeyCharacter(element):
        element = element['characters']
        if len(element) > 0:
            return element[0]['name']
        else:
            return element['title']

    if filter:
        if filter == 'date':
            layaway.sort(key=lambda x: x['onsaleDate'])
        elif filter in ['character', 'characters']:
            layaway.sort(key=sortKeyCharacter)
        else:
            layaway.sort(key=lambda x: x['title'])
    
    response = {
        'data': {'layaway': layaway, 'total': len(layaway)},
        'code': 200
    }

    return response
