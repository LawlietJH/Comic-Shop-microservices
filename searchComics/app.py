from flask import Blueprint, make_response, jsonify
from config import createApp
import requests
import hashlib
import time
import os

app = createApp()

api = Blueprint('searchComics', __name__, url_prefix='/api/v1')

jsonResponse = lambda data, code: make_response(jsonify(data), code)
characters_list = None

#--------------------------------------------------------------
# Utilidades:

def getURI(page=0, uri_type='characters'):

    API_PUB_KEY  = os.getenv('MARVEL_API_PUBLIC_KEY')
    API_PRIV_KEY  = os.getenv('MARVEL_API_PRIVATE_KEY')
    timestamp = int(time.time())
    input_string = str(timestamp) + API_PRIV_KEY + API_PUB_KEY
    API_HASH = hashlib.md5(input_string.encode("utf-8")).hexdigest()
    
    API_URL  = 'http://gateway.marvel.com/v1/public'
    API_PARAMS = f'ts={timestamp}&apikey={API_PUB_KEY}&hash={API_HASH}'
    URI_characters = f'{API_URL}/characters?{API_PARAMS}'
    URI_comics = f'{API_URL}/comics?{API_PARAMS}&format=comic&formatType=comic&noVariants=true'
    limit = '&limit=100&offset={}'
    URI = None
    if uri_type == 'characters':
        URI = URI_characters
    else:
        URI = URI_comics
    if URI and page >= 0:
        URI = URI + limit.format(page*100)
        return URI
    return

def getAllCharacters():
    
    output = {'characters': [], 'total': 0}

    # Lista todos los personajes:
    URI = getURI()
    
    response = requests.get(URI)
    response_json = response.json()
    status_code = response.status_code

    if status_code == 200:

        results = response_json['data']['results']
        total_characters = response_json['data']['total']
        total_pages = total_characters//100
        total_pages += 1 if total_pages % 100 > 0 else 0

        if total_characters > 0:

            characters = [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'image': f"{item['thumbnail']['path']}.{item['thumbnail']['extension']}",
                    'appearances': item['comics']['available']
                } for item in results
            ]

            output['characters'].extend(characters)

            if total_pages > 1:

                for page in range(1, total_pages):

                    URI = getURI(page)
                    response = requests.get(URI)
                    response_json = response.json()
                    status_code = response.status_code

                    if status_code == 200:

                        results = response_json['data']['results']

                        characters = [
                            {
                                'id': item['id'],
                                'name': item['name'],
                                'image': f"{item['thumbnail']['path']}.{item['thumbnail']['extension']}",
                                'appearances': item['comics']['available']
                            } for item in results
                        ]

                        output['characters'].extend(characters)
                    else:
                        return response_json
    
        output['total'] = len(output['characters'])
    
    else:
        return response_json
    
    return output

def getCharacters(words):
    
    output = {'characters': [], 'total': 0}

    # Busqueda de personajes:
    URI = getURI() + '&nameStartsWith=' + words
    
    response = requests.get(URI)
    response_json = response.json()
    status_code = response.status_code

    if status_code == 200:

        results = response_json['data']['results']
        total_characters = response_json['data']['total']
        total_pages = total_characters//100
        total_pages += 1 if total_pages % 100 > 0 else 0

        if total_characters > 0:

            characters = [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'image': f"{item['thumbnail']['path']}.{item['thumbnail']['extension']}",
                    'appearances': item['comics']['available']
                } for item in results
            ]

            output['characters'].extend(characters)

            if total_pages > 1:

                for page in range(1, total_pages):

                    URI = getURI(page) + '&nameStartsWith=' + words
                    response = requests.get(URI)
                    response_json = response.json()
                    status_code = response.status_code

                    if status_code == 200:

                        results = response_json['data']['results']

                        characters = [
                            {
                                'id': item['id'],
                                'name': item['name'],
                                'image': f"{item['thumbnail']['path']}.{item['thumbnail']['extension']}",
                                'appearances': item['comics']['available']
                            } for item in results
                        ]

                        output['characters'].extend(characters)
                    else:
                        return response_json
    
        output['total'] = len(output['characters'])
    
    else:
        return response_json
    
    return output

def getComics(words):
    
    output = {'comics': [], 'total': 0}

    # Busqueda de comics:
    URI = getURI(uri_type='comics') + '&titleStartsWith=' + words
    
    response = requests.get(URI)
    response_json = response.json()
    status_code = response.status_code

    if status_code == 200:

        results = response_json['data']['results']
        total_comics = response_json['data']['total']
        total_pages = total_comics//100
        total_pages += 1 if total_pages % 100 > 0 else 0

        if total_comics > 0:

            comics = [
                {
                    'id': item['id'],
                    'title': item['title'],
                    'image': f"{item['thumbnail']['path']}.{item['thumbnail']['extension']}",
                    'onsaleDate': [obj['date'] for obj in item['dates'] if obj.get('type') == 'onsaleDate'].pop()
                } for item in results
            ]

            output['comics'].extend(comics)

            if total_pages > 1:

                for page in range(1, total_pages):

                    URI = getURI(page, uri_type='comics') + '&titleStartsWith=' + words
                    response = requests.get(URI)
                    response_json = response.json()
                    status_code = response.status_code

                    if status_code == 200:
                        results = response_json['data']['results']
                        comics = [
                            {
                                'id': item['id'],
                                'title': item['title'],
                                'image': f"{item['thumbnail']['path']}.{item['thumbnail']['extension']}",
                                'onsaleDate': [obj['date'] for obj in item['dates'] if obj.get('type') == 'onsaleDate'].pop()
                            } for item in results
                        ]
                        output['comics'].extend(comics)
                    else:
                        return response_json
        
        output['total'] = len(output['comics'])

    else:

        return response_json

    return output

#--------------------------------------------------------------
# Rutas:

@api.route('/searchComics/')
def showCharacters():

    global characters_list

    if not characters_list:
        print('Log: Cargando todos los personajes...')
        characters_list = getAllCharacters()

    return jsonResponse(characters_list, 200)

@api.route('/searchComics/<string:words>')
def searchComicsAndCharacters(words):

    characters = getCharacters(words)
    comics = getComics(words)

    if characters.get('characters') == None:
        return jsonResponse(characters, characters['code'])

    if comics.get('comics') == None:
        return jsonResponse(comics, comics['code'])

    if not characters and not comics:
        return jsonResponse({'message': 'Nothing found'}, 404)

    data = {
        'characters': characters['characters'],
        'comics': comics['comics'],
        'total': characters['total'] + comics['total']
    }

    return jsonResponse(data, 200)

@api.route('/searchComics/character/<string:character_name>')
def getCharacter(character_name):

    if character_name:
    
        # Busqueda de un personaje en especifico:
        URI = getURI() + '&name=' + character_name
        response = requests.get(URI)
        response_json = response.json()
        status_code = response.status_code

        if status_code == 200:

            item = response_json['data']['results']
            
            if item:

                item = item.pop()

                character = {
                    'id': item['id'],
                    'name': item['name'],
                    'image': f"{item['thumbnail']['path']}.{item['thumbnail']['extension']}",
                    'appearances': item['comics']['available']
                }

                return jsonResponse(character, 200)

            return jsonResponse({'message': 'Character not found'}, 404)
        
        return jsonResponse(response_json, status_code)
    
    return jsonResponse({'message': 'error'}, 400)

@api.route('/searchComics/comic/<string:comic_title>/<int:issue_number>')
def getComic(comic_title, issue_number):

    if comic_title and issue_number:
        
        # Busqueda de un comic en especifico:
        URI = getURI(uri_type='comics') + f'&title={comic_title}&issueNumber={issue_number}'
        response = requests.get(URI)
        response_json = response.json()
        status_code = response.status_code

        if status_code == 200:

            item = response_json['data']['results']
            
            if item:

                item = item.pop()
                
                for obj in item['dates']:
                    if obj.get('type') == 'onsaleDate':
                        onsaleDate = obj['date']

                comic = {
                    'id': item['id'],
                    'title': item['title'],
                    'image': f"{item['thumbnail']['path']}.{item['thumbnail']['extension']}",
                    'onsaleDate': onsaleDate
                }

                return jsonResponse(comic, 200)
            
            return jsonResponse({'message': 'Comic not found'}, 404)

        return jsonResponse(response_json, status_code)

    return jsonResponse({'error': "The 'title' and 'issueNumber' are needed to search for a specific comic"}, 409)


app.register_blueprint(api)

#--------------------------------------------------------------

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
