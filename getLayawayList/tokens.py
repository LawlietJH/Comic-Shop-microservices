from flask import request, make_response, jsonify
from db import getToken

jsonResponse = lambda data, code: make_response(jsonify(data), code)

def loginRequired(*args, **kwargs):

    without_params = len(args) == 1 and len(kwargs) == 0 and callable(args[0])
    
    func = None
    get_username = None

    if without_params:
        func = args[0]
    else:
        get_username = kwargs.get('get_username')

    def wrapper(*args, **kwargs):
        
        try:
            header_auth = request.headers['Authorization']
            header_auth = header_auth.split(' ')[-1]
        except:
            return jsonResponse({'message': 'Unauthorized. User token required'}, 401)
        
        token = getToken(token=header_auth)

        if not token:
            return jsonResponse({'message': 'Unauthorized. The user token is not valid'}, 401)
        
        token_value = token.get('token')

        if not header_auth == token_value:
            return jsonResponse({'message': 'Unauthorized. The user token is not valid'}, 401)

        if get_username:
            username = token.get('username')
            return func(username, *args, **kwargs)

        return func(*args, **kwargs)

    if without_params:
        wrapper.__name__ = func.__name__
        return wrapper
    else:
        def inner(function):
            nonlocal func
            func = function
            wrapper.__name__ = func.__name__
            return wrapper
        return inner
