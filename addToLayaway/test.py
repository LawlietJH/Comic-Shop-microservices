import unittest
import requests
from random import randint, choice

class APITest(unittest.TestCase):

    API_URL_USERS = 'http://localhost:5001/api/v1'
    API_URL_LAYAWAY = 'http://localhost:5002/api/v1'
    
    def test_addToLayaway(self):
        # Prueba Agregar un Comic a los Apartados del Usuario:
        #--------------------------------------
        # Obtiene el Token de un Usuario:
        URL = self.API_URL_USERS + '/users/login/'
        content = {
            'username': 'Deleon',
            'password': 'xD'
        }
        token = ''
        r = requests.post(URL, json=content)
        if r.status_code == 200:
            data = r.json()
            token = data.get('token')
        #--------------------------------------
        URL = self.API_URL_LAYAWAY + '/addToLayaway/'
        headers = {'Authorization': f'Bearer {token}'}
        content = {
            "title": choice(['Spider-Man', 'Deadpool', 'Black Widow']),
            "number": randint(1, 20)
        }
        r = requests.post(URL, json=content, headers=headers)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
