"""The route functions for the instance of user table."""
from flask import Blueprint, request, jsonify,current_app
from models import User, db, VerificationRequest
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import upload_images
import os
from captcha.image import ImageCaptcha
from datetime import datetime, timedelta
# from io import BytesIO
import uuid
import random
import string
import base64
import json
user_bp = Blueprint('user', __name__)


# 简单存储验证码的字典（生产环境请用 Redis 或数据库替代）

captcha_storage = {}  # 格式: {captcha_id: {"text": "验证码内容", "expires_at": 过期时间}}
def generate_captcha_text(length=4):
    """生成随机验证码文本"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@user_bp.route('/captcha', methods=['GET'])
def get_captcha():
    """生成图形验证码并返回"""
    captcha_text = generate_captcha_text()
    captcha_id = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(minutes=5)  # 设置5分钟有效期

    # 存储验证码内容和过期时间
    captcha_storage[captcha_id] = {"text": captcha_text, "expires_at": expires_at}

    # 生成图形验证码图片
    image = ImageCaptcha(width=280, height=90)
    image_data = image.generate(captcha_text)

    # 将图像数据转换为 Base64 格式
    base64_image = f"data:image/png;base64,{base64.b64encode(image_data.read()).decode('utf-8')}"

    return jsonify({"captcha_id": captcha_id, "image": base64_image}),200

@user_bp.route('/register', methods=['POST'])
def register():
    """注册用户并验证验证码"""
    data = request.get_json()
    phone = data.get('phone')
    input_captcha = data.get('captcha')
    captcha_id = data.get('captcha_id')

    if not phone or not input_captcha or not captcha_id:
        return jsonify({'error': 'Phone, captcha, and captcha_id are required'}), 400

    # 校验验证码
    stored_captcha = captcha_storage.get(captcha_id)
    if not stored_captcha:
        return jsonify({'error': 'Captcha expired or invalid'}), 400

    # 检查验证码是否过期
    if datetime.now() > stored_captcha["expires_at"]:
        captcha_storage.pop(captcha_id, None)
        return jsonify({'error': 'Captcha expired'}), 400

    # 校验验证码内容
    if input_captcha.upper() != stored_captcha["text"]:
        return jsonify({'error': 'Incorrect captcha'}), 400

    # 验证通过后删除验证码
    captcha_storage.pop(captcha_id, None)

    # 检查手机号是否已注册
    if User.query.filter_by(phone=phone).first():
        return jsonify({'error': 'Phone number already registered'}), 401

    # 创建新用户
    new_user = User(
        nickname=phone,
        phone=phone,
        bio=data.get('bio', '还没有设置个性签名噢~'),
        avatar=data.get('avatar', ''),
        is_admin=data.get('is_admin', False),
        is_forbidden=data.get('is_forbidden', False),
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """Log in the user.

    Returns:
        A json object consists of message.
    """
    data = request.get_json()
    user = User.query.filter_by(phone=data['phone']).first()
    if user and user.check_password(data['password']):
        if user.is_forbidden:
            return jsonify({'error': 'User is forbidden'}), 403
        if user.is_admin:
            return jsonify({'error': 'User is an admin, please register a user account'}), 403
        token = user.generate_token()
        return jsonify({'token': token, 'role': 'user','user_id':user.id}), 200
    return jsonify({'error': 'Invalid phone number or password'}), 400

@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Log out the user and invalidate the JWT token.
    
    Returns:
        A json object consists of message.
    """
    user_data = get_jwt_identity()
    user_data = json.loads(user_data)
    user = User.query.get(user_data['id'])
    if user:
        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户的个人资料，包括头像 URL"""
    # print(f"Authorization Header: {request.headers.get('Authorization')}")  # 打印 JWT
    user_data = get_jwt_identity()
    user_data = json.loads(user_data)
    user = User.query.get_or_404(user_data['id'])

    # 生成头像的完整 URL，如果头像存在
    if user.avatar:
        avatar_url = f"{request.host_url}{user.avatar}"
    else:
        # 如果用户没有上传头像，可以设置一个默认头像的 URL
        avatar_url = f"{request.host_url}static/default/default_avatar.png"

    return jsonify({
        'id': user.id,
        'nickname': user.nickname,
        'phone': user.phone,
        'bio': user.bio,
        'avatar': avatar_url,  # 返回头像的 URL
        'role': 'user' if not user.is_admin else 'admin',
        'auth_status': user.auth_status,
    }), 200

@user_bp.route('/get_info_by_user_id/<int:user_id>', methods=['GET'])
@jwt_required()
def get_info_by_user_id(user_id):
    """获取用户的个人资料，包括头像 URL"""
    # print(f"Authorization Header: {request.headers.get('Authorization')}")  # 打印 JWT
    user = User.query.get_or_404(user_id)

    # 生成头像的完整 URL，如果头像存在
    if user.avatar:
        avatar_url = f"{request.host_url}{user.avatar}"
    else:
        # 如果用户没有上传头像，可以设置一个默认头像的 URL
        avatar_url = f"{request.host_url}static/default/default_avatar.png"

    return jsonify({
        'id': user.id,
        'nickname': user.nickname,
        'phone': user.phone,
        'bio': user.bio,
        'avatar': avatar_url,  # 返回头像的 URL
        'role': 'user' if not user.is_admin else 'admin'
    }), 200

@user_bp.route('/profile/change_password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change the user's password.

    Returns:
        A json object consists of message.
    """
    data = request.get_json()

    user_data = get_jwt_identity()
    user_data = json.loads(user_data)
    user = User.query.get_or_404(user_data['id'])
    # print(data)
    if not check_password_hash(user.password_hash, data['old_password']):
        return jsonify({'error': 'Old password is incorrect'}), 400

    user.set_password(data['new_password'])
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'}), 200


@user_bp.route('/profile/edit_profile', methods=['POST'])
@jwt_required()
def edit_profile():
    """Edit the user's profile information such as nickname, bio, and avatar.

    Returns:
        A json object consists of message.
    """
    # 获取用户身份信息
    user_data = get_jwt_identity()  # 获取用户 ID
    user_data = json.loads(user_data)
    user = User.query.get_or_404(user_data['id'])

    # 获取请求体中的数据
    data = request.form  # 从请求体中获取前端提交的 form data
    # print("接收到的数据:", data)  # 打印接收到的数据，调试用

    # 更新用户信息
    if 'nickname' in data:
        user.nickname = data['nickname']
    if 'bio' in data:
        user.bio = data['bio']
    
    # 更新头像
    if 'avatar' in request.files:
        file = request.files['avatar']
        file_path = upload_images(file, user.id, upload_type="avatars")
        if not file_path:
            return jsonify({'error': '图像上传失败'}), 400
        # 如果已经有头像，删除旧头像文件
        if user.avatar and os.path.exists(user.avatar):
            os.remove(user.avatar)
        # 保存新头像文件
        user.avatar = file_path  # 更新数据库中的头像路径

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

