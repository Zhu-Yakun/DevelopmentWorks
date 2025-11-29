from functools import wraps
from flask import jsonify,request
from flask_jwt_extended import verify_jwt_in_request, jwt_required

# 登录限制的装饰器 用于某些只让登录用户查看的网
def login_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return func(*args, **kwargs)
        except Exception as e:
           return jsonify({'message': str(e)}), 401
    return wrapper