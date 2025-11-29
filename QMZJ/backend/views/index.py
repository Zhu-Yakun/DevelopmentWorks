from flask import Blueprint, session, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from models.User import User
from models.modelConfig import db
from decorators import login_limit


index = Blueprint("index", __name__, url_prefix="/api")


# 注册请求
@index.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    account = request.json['account']#把手机号当做账号
    password = request.json['password']
    
    if not username or not account or not password:
        return jsonify({"message": "缺少必要字段"}), 400  # Bad Request
    
    user = User.query.filter(User.account == account).first()
    if user is not None:
        return jsonify({"message": "该账号已存在"}), 409  # Conflict
    else:
        user = User(username=username, account=account)
        # 调用password_hash对密码加密
        user.password_hash(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "注册成功！"}), 201  # Created

# 登录请求
@index.route('/login', methods=['POST'])
def login():
    account = request.json['account']
    password = request.json['password']
    
    if not account or not password:
        return jsonify({"message": "缺少必要字段"}), 400  # Bad Request
    
    user = User.query.filter(User.account == account).first()
    # check_password_hash比较两个密码是否相同
    if (user is not None) and (check_password_hash(user.password, password)):
        access_token = create_access_token(identity=user.id)
        response = jsonify({'access_token': access_token})
        response.set_cookie('access_token', access_token, httponly=True)
        print(response.data)
        return response
    else:
        return jsonify({"message": "账号或密码错误"}), 401  # Unauthorized


# 退出
@index.route('/logout', methods=['GET'])
@login_limit
def logout():
     # 从请求中获取存储在客户端的令牌
    token = request.cookies.get('access_token')

    # 如果存在令牌，删除令牌
    if token:
        response = jsonify({'message': 'You have been logged out successfully.'})
        response.delete_cookie('access_token')
        return response,200  # OK
    else:
        return jsonify({'message': 'No active session found.'})

