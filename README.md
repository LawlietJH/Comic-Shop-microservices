# Comic-Shop-microservices
Prueba técnica de microservicios en Python

## Contenido

- [Comic-Shop-microservices](#comic-shop-microservices)
	- [Contenido](#contenido)
	- [Microservicios](#microservicios)
		- [Microservicio: Search Comics](#microservicio-search-comics)
		- [Microservicio: Users](#microservicio-users)
		- [Microservicio: Add To Layaway](#microservicio-add-to-layaway)
		- [Microservicio: Get Layaway List](#microservicio-get-layaway-list)
	- [Docker](#docker)

---

## Microservicios

El proyecto cuenta con 4 microservicios los cuales son REST API:
* Microservicio: Search Comics
* Microservicio: Users
* Microservicio: Add To Layaway
* Microservicio: Get Layaway List

---

### Microservicio: Search Comics

Este microservicio está enfocado en la busqueda de Cómics. Es alimentado por la API de Marvel y consta de 4 funcionalidades:
* Listado Completo de Personajes.
* Búsqueda por Palabra (Cómics y Personajes).
* Obtención de Personaje por Nombre en específico.
* Obtención de Cómic por Título en específico.

Detalles de cada punto:

1\. Listado de todos los *Personajes* de Marvel (de la A a la Z):
* GET: **/api/v1/searchComics/**

Al no tener ningún criterio de búsqueda, se obtienen todos los personajes existentes.

Resultados (200 OK): 

Nota: Puede tardar varios segundos la primera vez.

```json
{
	"characters": [
		{
			"appearances": 12,
			"id": 1011334,
			"image": "http://i.annihil.us/u/prod/marvel/i/mg/c/e0/535fecbbb9784.jpg",
			"name": "3-D Man"
		},
		{
			"appearances": 4,
			"id": 1017100,
			"image": "http://i.annihil.us/u/prod/marvel/i/mg/3/20/5232158de5b16.jpg",
			"name": "A-Bomb (HAS)"
		},
        ...
    ],
    "total": 1562
}
```

2\. Busqueda por alguna Palabra:
* **/api/v1/searchComics/\<Palabra\>**

Entrega todos los *Cómics* y *Personajes* que comiencen por esa palabra.

Ejemplo:
* GET: **/api/v1/searchComics/Deadpool**

Resultados (200 OK):
```json
{
	"characters": [
		{
			"appearances": 867,
			"id": 1009268,
			"image": "http://i.annihil.us/u/prod/marvel/i/mg/9/90/5261a86cacb99.jpg",
			"name": "Deadpool"
		},
        ...
	],
	"comics": [
		{
			"id": 101090,
			"image": "http://i.annihil.us/u/prod/marvel/i/mg/3/60/624f475bb9114.jpg",
			"onsaleDate": "2022-08-31T00:00:00-0400",
			"title": "Deadpool: Bad Blood (2022) #4"
		},
		...
	],
	"total": 461
}
```

Se entrega los Personajes y los Cómics por separado, y un contador total de elementos.

3\. Filtro por Nombre de Personaje (nombre específico):
* **/api/v1/searchComics/character/\<Nombre\>**

Ejemplo:
* GET: **/api/v1/searchComics/character/Spider-Man (Peter Parker)**

Resultados (200 OK):
```json
{
	"appearances": 4154,
	"id": 1009610,
	"image": "http://i.annihil.us/u/prod/marvel/i/mg/3/50/526548a343e4b.jpg",
	"name": "Spider-Man (Peter Parker)"
}
```

4\. Filtro por *Título* (título específico y número de Cómic):
* **/api/v1/searchComics/character/\<Título\>/\<Número\>**

Ejemplo:
* GET: **/api/v1/searchComics/comic/Spider-Man/1**

Resultados (200 OK):
```json
{
	"id": 10767,
	"image": "http://i.annihil.us/u/prod/marvel/i/mg/6/e0/5bc76088e860c.jpg",
	"onsaleDate": "1990-08-01T00:00:00-0400",
	"title": "Spider-Man (1990) #1"
}
```

---

### Microservicio: Users

Este microservicio está enfocado en la administración de usuarios y consta de 3 funcionalidades:

* Crear un Usuario.
* Login: Obtiene un Token e información del Usuario.
* Obtención de información detallada del Usuario mediante su Token.

Detalles de cada punto:

1\. Creación de un Usuario sin requisitos. Esta funcionalidad permite que cualquier usuario se registre en la base de datos:
* POST: **/api/v1/users/**

Ejemplo (JSON):
```json
{
	"username": "Deleon",
	"password": "P4SSW0RD",
	"first_name": "Deleon",
	"last_name": "Lawliet",
	"age": 26
}
```

Resultados (201 CREATED):
```json
{
	"_id": "62f7682bb59f5ccc6062bc49",
	"age": 26,
	"first_name": "Deleon",
	"last_name": "Lawliet",
	"password": "pbkdf2:sha256:260000$QqhBlX7zKU7Cn1zK$9d352058dc4efd3e49...",
	"username": "Lawliet"
}
```

2\. Para obtener una sesión de usuario, debe hacerse login y obtendrá un Token:
* POST: **/api/v1/users/login**

Ejemplo:
```json
{
	"username": "Lawliet",
	"password": "P4SSW0RD"
}
```

Resultados (200 OK):
```json
{
	"age": 26,
	"id": "62f7682bb59f5ccc6062bc49",
	"name": "Deleon Lawliet",
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ikxhd2x...",
	"username": "Deleon"
}
```

3\. Si se desea obtener un listado detallado de la información del usuario, le pasamos el token:
* GET: **/api/v1/users/**
* Headers: **Authorization: Bearer \<Token\>**

Resultados (200 OK):
```json
{
	"_id": "62f7682bb59f5ccc6062bc49",
	"age": 26,
	"first_name": "Deleon",
	"last_name": "Lawliet",
	"username": "Deleon"
}
```

---

### Microservicio: Add To Layaway

Este microservicio está enfocado en agregar Cómics a la lista de Apartados del Usuario y cuenta con 1 funcionalidad:

* Agregar un Cómic a la Lista de Apartados.

Esta funcionalidad requiere un Token y un JSON que contenga el ID del Cómic que se desea agregar. El ID lo podemos obtener con el microservicio de busqueda (Search Cómics) y el token con el microservicio de usuarios (Users).

Ejemplo:

Agregaré el Cómic de Spider-Man #1 con ID '10767' (obtenido en el ejemplo de busqueda de un cómic en específico).

* POST: **/api/v1/addToLayaway/**
* Headers: **Authorization: Bearer \<Token\>**

```json
{
	"comic_id": 10767
}
```

Resultados (200 OK):
```json
{
	"comic": {
		"characters": [
			{
				"id": 1009610,
				"name": "Spider-Man (Peter Parker)"
			}
		],
		"id": 10767,
		"image": "http://i.annihil.us/u/prod/marvel/i/mg/6/e0/5bc76088e860c.jpg",
		"onsaleDate": "1990-08-01T00:00:00-0400",
		"title": "Spider-Man (1990) #1"
	},
	"message": "Comic added successfully"
}
```

---

### Microservicio: Get Layaway List

Este microservicio está enfocado en la obtención de todos los Cómics Apartados por el Usuario y consta de 2 Funcionalidades:

* Listado de todos los Apartados por el Usuario en orden de inserción.
* Listado con ordenamiento por Orden alfabético (título), personajes o fecha.

1\. El listado, sin filtro, mostrará todos los apartados en el orden de inserción de los datos.

Ejemplo:

* GET: **/api/v1/getLayawayList/**
* Headers: **Authorization: Bearer \<Token\>**

Resultados (200 OK):
```json
{
	"layaway": [
		{
			"characters": [
				{
					"id": 1009610,
					"name": "Spider-Man (Peter Parker)"
				}
			],
			"id": 10767,
			"image": "http://i.annihil.us/u/prod/marvel/i/mg/6/e0/5bc76088e860c.jpg",
			"onsaleDate": "1990-08-01T00:00:00-0400",
			"title": "Spider-Man (1990) #1"
		},
		{
			"characters": [
				{
					"id": 1009268,
					"name": "Deadpool"
				}
			],
			"id": 8457,
			"image": "http://i.annihil.us/u/prod/marvel/i/mg/e/b0/4bb6224caeea5.jpg",
			"onsaleDate": "1994-08-10T00:00:00-0400",
			"title": "Deadpool (1994) #1"
		}
	],
	"total": 2
}
```

2\. El listado con filtro se puede utilizar de la siguiente manera:

Filtros:
* title
* characters
* date

URI: **/api/v1/getLayawayList/<filter>**

Ejemplos:

Filtrar por orden alfabético (title):

* GET: **/api/v1/getLayawayList/title**
* Headers: **Authorization: Bearer \<Token\>**

Resultados (200 OK):
```json
{
	"layaway": [
		{
            ...
			"title": "Deadpool (1994) #1"
		},
		{
			...
			"title": "Spider-Man (1990) #1"
		}
	],
	"total": 2
}
```

Filtrar por orden alfabético (title):

* GET: **/api/v1/getLayawayList/characters**
* Headers: **Authorization: Bearer \<Token\>**

Resultados (200 OK):
```json
{
	"layaway": [
		{
			"characters": [
				{
					"id": 1009268,
					"name": "Deadpool"
				}
			],
			...
		},
		{
			"characters": [
				{
					"id": 1009610,
					"name": "Spider-Man (Peter Parker)"
				}
			],
			...
		}
	],
	"total": 2
}
```

Podemos comprobar que los datos son ordenados por personaje (character['name']).

Filtrar por fecha (date):

* GET: **/api/v1/getLayawayList/date**
* Headers: **Authorization: Bearer \<Token\>**

Resultados (200 OK):
```json
{
	"layaway": [
		{
			...
			"onsaleDate": "1990-08-01T00:00:00-0400",
			"title": "Spider-Man (1990) #1"
		},
		{
			...
			"onsaleDate": "1994-08-10T00:00:00-0400",
			"title": "Deadpool (1994) #1"
		}
	],
	"total": 2
}
```

Podemos comprobar que los datos son ordenados por la fecha (onsaleDate).

Notas:
* Tomé en cuenta que los archivos **.env** no deberían mostrarse por cuestiones de seguridad, pero por fines prácticos los deje (tomé en cuenta que no hay problema en mostrar los datos).
* Las **Pruebas Unitarias** de cada microservicio las realicé mediante la librería (módulo) Unittest y están alojadas en los archivos **test.py**.

---

## Docker

Para correr todas las imagenes:

Docker Pull:

	docker pull enylaine/comic-shop-search:latest
	docker pull enylaine/comic-shop-users:latest
	docker pull enylaine/comic-shop-addtolayaway:latest
	docker pull enylaine/comic-shop-getlayawaylist:latest

Docker Run:

    docker run -d -p 5000:5000 enylaine/comic-shop-search
    docker run -d -p 5001:5001 enylaine/comic-shop-users
    docker run -d -p 5002:5002 enylaine/comic-shop-addtolayaway
    docker run -d -p 5003:5003 enylaine/comic-shop-getlayawaylist

Notas:

* Con el parámetro **-d** (*--detach*) ejecuta el contenedor en segundo plano e imprime el ID del contenedor.
* Cambiando el parámetro *-d* por el parámetro **-it** (*--interactive* y *--tty*) mantiene el STDIN abierto incluso si no está conectada y se le asigna una pseudo-TTY, de esta forma se puede mostrar los logs y respuestas del servidor. Ejemplo: **docker run -it -p 5000:5000 enylaine/comic-shop-search**
