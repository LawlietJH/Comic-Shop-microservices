import unittest
import requests

class APITest(unittest.TestCase):

    API_URL = 'http://localhost:5000/api/v1'
    
    def test_showCharacters(self):
        # Prueba obtener la lista completa de Personajes:
        URL = self.API_URL + '/searchComics/'
        r = requests.get(URL)
        data = r.json()
        total = data.get('total')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(total, 1562)
    
    def test_searchComicsAndCharacters(self):
        # Prueba obtener una lista de Personajes y Comic que coincidan una palabra:
        search = 'Cat'
        URL = self.API_URL + f'/searchComics/{search}'
        r = requests.get(URL)
        data = r.json()
        total = data.get('total')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(total, 16)
    
    def test_getCharacter(self):
        # Prueba obtener un Personaje en Especifico:
        character = 'Spider-Man (Peter Parker)'
        URL = self.API_URL + f'/searchComics/character/{character}'
        r = requests.get(URL)
        data = r.json()
        id = data.get('id')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(id, 1009610)
    
    def test_getComic(self):
        # Prueba obtener un Comic en Especifico:
        comic = 'Spider-Man'
        issueNum = '1'
        URL = self.API_URL + f'/searchComics/comic/{comic}/{issueNum}'
        r = requests.get(URL)
        data = r.json()
        id = data.get('id')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(id, 10767)

if __name__ == '__main__':
    unittest.main()