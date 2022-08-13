from flask import Blueprint, request, make_response, jsonify
from config import createApp
from tokens import loginRequired
from db import addComic
import requests
import hashlib
import time
import os

app = createApp()

api = Blueprint('addToLayaway', __name__, url_prefix='/api/v1')

jsonResponse = lambda data, code: make_response(jsonify(data), code)

#--------------------------------------------------------------
# Utilidades:

def getComicURI(comic_id):

    API_PUB_KEY  = os.getenv('MARVEL_API_PUBLIC_KEY')
    API_PRIV_KEY  = os.getenv('MARVEL_API_PRIVATE_KEY')
    timestamp = int(time.time())
    input_string = str(timestamp) + API_PRIV_KEY + API_PUB_KEY
    API_HASH = hashlib.md5(input_string.encode("utf-8")).hexdigest()
    API_URL  = 'http://gateway.marvel.com/v1/public'
    API_PARAMS = f'ts={timestamp}&apikey={API_PUB_KEY}&hash={API_HASH}'
    
    URI = f'{API_URL}/comics/{comic_id}?{API_PARAMS}'
    
    return URI

def getComic(comic_URI):
    
    resp = requests.get(comic_URI)
    
    if not resp.status_code == 200:
        return {
            'data': {'message': 'The Comic of the ID does not exist'},
            'code': 400
        }
    
    content = resp.json()
    content = content['data']['results'].pop()

    onsaleDate = ''

    for obj in content['dates']:
        if obj.get('type') == 'onsaleDate':
            onsaleDate = obj['date']

    characters = []
    for obj in content['characters']['items']:
        character = {
            'id': int(obj['resourceURI'].split('/')[-1]),
            'name': obj['name']
        }
        characters.append(character)
    
    # if characters:
    #     characters.sort(key=lambda x: x['id'])

    response = {
        'data': {
            'id': content['id'],
            'title': content['title'],
            'image': f"{content['thumbnail']['path']}.{content['thumbnail']['extension']}",
            'onsaleDate': onsaleDate,
            'characters': sorted(characters, key=lambda x: x['id'])
        },
        'code': 200
    }

    return response

#--------------------------------------------------------------
# Rutas:

@api.route('/addToLayaway/', methods=['POST'])
@loginRequired(get_username=True)
def addToLayaway(username):
    
    comic_id = request.json.get('comic_id')

    if not comic_id:
        return jsonResponse({'comic_id': 'This field is required'}, 400)
    
    comic_URI = getComicURI(comic_id)
    
    resp = getComic(comic_URI)

    if not resp['code'] == 200:
        return jsonResponse(response['data'], response['code'])
    
    comic = resp['data']

    response = addComic(username, comic)
    
    return jsonResponse(response['data'], response['code'])


app.register_blueprint(api)

#--------------------------------------------------------------

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5002)
