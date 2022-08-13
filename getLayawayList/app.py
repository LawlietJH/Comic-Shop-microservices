from flask import Blueprint, make_response, jsonify
from config import createApp
from tokens import loginRequired
from db import getComicList

app = createApp()

api = Blueprint('getLayawayList', __name__, url_prefix='/api/v1')

jsonResponse = lambda data, code: make_response(jsonify(data), code)

#--------------------------------------------------------------
# Rutas:

@api.route('/getLayawayList/')
@loginRequired(get_username=True)
def getLayawayList(username):
    
    response = getComicList(username)
    
    return jsonResponse(response['data'], response['code'])

@api.route('/getLayawayList/<string:ordering>')
@loginRequired(get_username=True)
def getLayawayListSorted(username, ordering):
    
    response = getComicList(username, ordering)
    
    return jsonResponse(response['data'], response['code'])


app.register_blueprint(api)

#--------------------------------------------------------------

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5003)
