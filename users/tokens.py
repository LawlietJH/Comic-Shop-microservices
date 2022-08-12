from flask import request, make_response, jsonify
from db import getToken

jsonResponse = lambda data, code: make_response(jsonify(data), code)



def loginRequired(*args, **kwargs):

    with_params = len(args) == 1 and len(kwargs) == 0 and callable(args[0])
    
    func = None
    get_username = None

    if with_params:
        func = args[0]
    else:
        get_username = kwargs.get('get_username')

    def wrapper(*args, **kwargs):
        
        not_authorized = jsonResponse({'message': 'Unauthorized'}, 401)

        try:
            header_auth = request.headers['Authorization']
            header_auth = header_auth.split(' ')[-1]
        except:
            return not_authorized
        
        token = getToken(token=header_auth)

        if not token:
            return not_authorized
        
        token_value = token.get('token')

        if not header_auth == token_value:
            return not_authorized

        if get_username:
            username = token.get('username')
            return func(username, *args, **kwargs)

        return func(*args, **kwargs)

    if with_params:
        return wrapper
    else:
        def inner(function):
            nonlocal func
            func = function
            return wrapper
        return inner

    