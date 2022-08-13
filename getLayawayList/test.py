import unittest
import requests
from random import randint, choice

def getToken():
    API_URL = 'http://localhost:5001/api/v1'
    URL = API_URL + '/users/login/'
    content = {'username': 'Deleon', 'password': 'xD'}
    token = ''
    r = requests.post(URL, json=content)
    if r.status_code == 200:
        data = r.json()
        token = data.get('token')
    return token

class APITest(unittest.TestCase):

    API_URL_LAYAWAY_LIST = 'http://localhost:5003/api/v1'
    
    def test_getLayawayList(self):
        # Prueba Agregar un Comic a los Apartados del Usuario:
        #--------------------------------------
        # Obtiene el Token de un Usuario:
        token = getToken()
        #--------------------------------------
        URL = self.API_URL_LAYAWAY_LIST + '/getLayawayList/'
        headers = {'Authorization': f'Bearer {token}'}
        content = {
            "title": choice(['Spider-Man', 'Deadpool', 'Black Widow']),
            "number": randint(1, 20)
        }
        r = requests.post(URL, json=content, headers=headers)
        self.assertEqual(r.status_code, 200)
    
    def test_getSortedLayawayList(self):
        # Prueba Agregar un Comic a los Apartados del Usuario:
        #--------------------------------------
        # Obtiene el Token de un Usuario:
        token = getToken()
        #--------------------------------------
        URL = self.API_URL_LAYAWAY_LIST + '/getLayawayList/title'
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.post(URL, headers=headers)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
