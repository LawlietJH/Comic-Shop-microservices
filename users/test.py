import unittest
import requests
from random import choices
from string import ascii_letters

randomString = lambda length: ''.join(choices(ascii_letters, k=length))

class APITest(unittest.TestCase):

    API_URL = 'http://localhost:5000'
    username = None
    password = None
    token = None
    
    def test_1_createUser(self):
        # Prueba Crear un Usuario:
        URL = self.API_URL + '/users/'
        self.username = randomString(5)
        self.password = randomString(6)
        content = {
            "username": self.username,
            "password": self.password,
            "first_name": randomString(4),
            "last_name": randomString(7),
            "age": 30
        }
        r = requests.post(URL, json=content)
        self.assertEqual(r.status_code, 201)
    
    def test_2_login(self):
        # Prueba de Inicio de Sesión:
        URL = self.API_URL + '/users/login/'
        if self.username and self.password:
            content = {
                "username": self.username,
                "password": self.password
            }
        else:
            content = {
                "username": "Deleon",
                "password": "xD"
            }
        r = requests.post(URL, json=content)
        data = r.json()
        token = data.get('token')
        if token:
            self.token = token
        self.assertEqual(r.status_code, 200)

    def test_3_getUserInfo(self):
        # Prueba obtener la información del usuario autenticado:
        URL = self.API_URL + '/users/'
        if self.token:
            token = self.token
        else:
            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkRlbGVvbiIsImV4cCI6MTY2MDg1ODgxMH0.zDys5qRtVrvQFGABNCWzwcfd0eSA-Rg_W_1aeEGz1z4'
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.get(URL, headers=headers)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
