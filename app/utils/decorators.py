from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

# Custom decorator created to be able to require roles for certain routes
def role_required(required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] not in required_roles:
                return jsonify({"msg": "Access denied"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
