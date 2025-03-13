"""The routes for admin."""
from flask import Blueprint, jsonify, request
from models import User,Friendship,Message
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators import admin_required
import os
import json

admin_bp = Blueprint('admin', __name__)



@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """检查用户是否是管理员，并生成 JWT 令牌。
    
    Returns:
        A json object consists of message and JWT token.
    """
    data = request.get_json()
    
    # 检查传递的参数是否包含手机号码和密码
    if not data or 'phone' not in data or 'password' not in data:
        return jsonify({'error': 'Missing phone or password'}), 400

    # 查找数据库中的用户
    user = User.query.filter_by(phone=data['phone']).first()
    
    # 如果用户存在并且密码正确
    if user and user.check_password(data['password']):
        # 检查该用户是否为管理员
        if user.is_admin:
            # 生成JWT令牌
            token = user.generate_token()
            return jsonify({
                'message': 'Admin login successful',
                'token': token,
                'role': 'admin'
            }), 200
        else:
            return jsonify({'error': 'User is not an admin'}), 403
    else:
        return jsonify({'error': 'Invalid phone number or password'}), 400
    
@admin_bp.route('/logout', methods=['POST'])
@jwt_required()
def admin_logout():
    """注销用户，使JWT令牌失效。
    
    Returns:
        A json object consists of message.
    """
    # 从JWT令牌中获取用户信息
    user_data = get_jwt_identity()
    user_data = json.loads(user_data)
    # 使JWT令牌失效
    user = User.query.get(user_data['id'])
    if user:
        return jsonify({'message': 'Logout successful'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/profile', methods=['GET'])
@admin_required
def get_admin():
    """Get the user's information based on JWT token.
    
    Returns:
        A json object consists of message.
    """
    admin_data = get_jwt_identity()
    admin_data = json.loads(admin_data)
    # print(admin_data)
    user = User.query.get_or_404(admin_data['id'])

    # 生成头像的完整 URL，如果头像存在
    if user.avatar:
        avatar_url = f"{request.host_url}{user.avatar}"
    else:
        # 如果用户没有上传头像，可以设置一个默认头像的 URL
        avatar_url = f"{request.host_url}static/default/default_avatar.png"

    return jsonify({
        'nickname': user.nickname,
        'phone': user.phone,
        'bio': user.bio,
        'avatar': avatar_url,
        'role': 'admin' if user.is_admin else 'user',
    }),200


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_non_admin_users():
    """获取所有非管理员用户信息。
    
    Returns:
        A json object consists of message and a list of non-admin users.
    """
    # 查询所有非管理员用户
    non_admin_users = User.query.filter_by(is_admin=False).all()
    
    return jsonify([{
        'id': user.id,
        'avatar': f"{request.host_url}{user.avatar}" if user.avatar else f"{request.host_url}static/default/default_avatar.png",
        'nickname': user.nickname,
        'phone': user.phone,
        'bio': user.bio,
        'role': 'user',
        'status': 'forbid' if user.is_forbidden else 'normal'
    } for user in non_admin_users]), 200


@admin_bp.route('/users/<int:id>/delete', methods=['DELETE'])
@admin_required
def delete_user(id):
    """删除指定用户。
    
    Returns:
        A json object consists of message.
    """
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    avatar_path = user.avatar
    if avatar_path != 'static/default/default_avatar.png':
        # 删除用户头像
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
            if os.path.exists(os.path.dirname(avatar_path)):
                for file in os.listdir(os.path.dirname(avatar_path)):
                    os.remove(os.path.join(os.path.dirname(avatar_path), file))
                os.rmdir(os.path.dirname(avatar_path))
    Friendship.query.filter((Friendship.user_id == user.id) | (Friendship.friend_id == user.id)).delete()
    Message.query.filter((Message.sender_id == user.id) | (Message.receiver_id == user.id)).delete()
    
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


@admin_bp.route('/users/<int:id>/forbid', methods=['PATCH'])
@admin_required
def forbid_user(id):
    """禁止指定用户。
    
    Returns:
        A json object consists of message.
    """
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.is_forbidden = True
    db.session.commit()
    return jsonify({'message': 'User forbidden successfully'}), 200

@admin_bp.route('/users/<int:id>/unforbid', methods=['PATCH'])
@admin_required
def unforbid_user(id):
    """解除指定用户的禁止状态。
    
    Returns:
        A json object consists of message.
    """
    user = User.query.get(id)    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.is_forbidden = False
    db.session.commit()
    return jsonify({'message': 'User unforbidden successfully'}), 200
