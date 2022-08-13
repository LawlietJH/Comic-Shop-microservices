from flask import Blueprint, request, make_response, jsonify
from config import createApp
from tokens import loginRequired
from db import addComic
import requests

app = createApp()

api = Blueprint('addToLayaway', __name__, url_prefix='/api/v1')

jsonResponse = lambda data, code: make_response(jsonify(data), code)

#--------------------------------------------------------------
# Rutas:

@api.route('/addToLayaway/', methods=['POST'])
@loginRequired(get_username=True)
def addToLayaway(username):
    
    title = request.json.get('title')
    number = request.json.get('number')

    error_response = {}

    if not title:
        error_response['title'] = 'This field is required'
    if not number:
        error_response['number'] = 'This field is required'

    if error_response:
        return jsonResponse(error_response, 400)
    
    res = requests.get(f'http://localhost:5000/api/v1/searchComics/comic/{title}/{number}')
    
    if not res.status_code == 200:
        return jsonResponse({'message': 'The Comic does not exist'}, 400)
    
    comic = res.json()

    response = addComic(username, comic)
    
    return jsonResponse(response['data'], response['code'])


app.register_blueprint(api)

#--------------------------------------------------------------

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5002)
