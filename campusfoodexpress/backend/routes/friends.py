from flask import Blueprint, jsonify, request
from extensions import db
from models import Friendship, User, Message, Status
from flask_jwt_extended import jwt_required, get_jwt_identity
from .chat import get_unread_count
from datetime import datetime, timezone
import json
friend_bp = Blueprint('friend', __name__)

@friend_bp.route('/add', methods=['POST'])
@jwt_required()
def add_friend():
    """
    Route to add a friend for the current user.
    Request body:
    {
        "friend_id": int  # The ID of the user to be added as a friend
    }
    """
    # Get the current user's identity
    current_user_id = json.loads(get_jwt_identity()).get('id')
    if not current_user_id:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    friend_id = data.get('friend_id')

    if not friend_id:
        return jsonify({"message": "Friend ID is required"}), 400

    if friend_id == current_user_id:
        return jsonify({"message": "You cannot add yourself as a friend"}), 400

    # Check if the friend exists
    friend = User.query.filter_by(id=friend_id,is_admin = False).first()
    if not friend:
        return jsonify({"message": "Friend not found"}), 404

    # Check if the friendship already exists
    existing_friendship = Friendship.query.filter_by(user_id=current_user_id, friend_id=friend_id).first()
    if existing_friendship:
        return jsonify({"message": "Friendship already exists"}), 400

    # Add the friendship
    new_friendship = Friendship(user_id=current_user_id, friend_id=friend_id)
    db.session.add(new_friendship)

    # Optional: Create a reverse friendship if friendships are bidirectional
    reverse_friendship = Friendship.query.filter_by(user_id=friend_id, friend_id=current_user_id).first()
    if not reverse_friendship:
        reverse_friendship = Friendship(user_id=friend_id, friend_id=current_user_id)
        db.session.add(reverse_friendship)

    db.session.commit()

    return jsonify({"message": "Friend added successfully"}), 201


@friend_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_friend():
    """
    API endpoint to delete a friend.
    Request body:
        {
            "friend_id": int  # ID of the friend to be removed
        }
    """
    # Get the current user's ID from the JWT
    user_id = json.loads(get_jwt_identity()).get('id')

    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # Parse request data
    data = request.get_json()
    friend_id = data.get('friend_id')

    if not friend_id:
        return jsonify({'error': 'Friend ID is required'}), 400

    # Check if the friendship exists
    friendship = Friendship.query.filter_by(user_id=user_id, friend_id=friend_id).first()
    if not friendship:
        return jsonify({'error': 'Friendship not found'}), 404

    # Optional: Also delete the reverse friendship if bidirectional relationships are used
    reverse_friendship = Friendship.query.filter_by(user_id=friend_id, friend_id=user_id).first()
    if reverse_friendship:
        db.session.delete(reverse_friendship)

    # Delete the friendship
    db.session.delete(friendship)
    db.session.commit()

    return jsonify({'message': 'Friend deleted successfully'}), 200


@friend_bp.route('/friends', methods=['GET'])
@jwt_required()
def get_friends():
    """
    Get the list of friends for the logged-in user, with optional search.
    Returns all details about friends including avatar, bio, and more.
    Query parameters:
        - search (optional): A keyword to filter friends by nickname or phone.
    """
    user_id = json.loads(get_jwt_identity()).get('id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # Get the search query from the request
    search_query = request.args.get('search', '').strip()

    # Fetch friendships where the user is the current user
    friends=[]
    friendships = Friendship.query.filter_by(user_id=user_id).all()
    unread_counts = get_unread_count(user_id)
    # 获取每一个亲友的最新消息
    for friendship in friendships:
        if friendship.friend.is_forbidden:
            continue
        last_message = Message.query.filter(
            ((Message.sender_id == friendship.friend.id) & (Message.receiver_id == user_id)) |
            ((Message.sender_id == user_id) & (Message.receiver_id == friendship.friend.id))
        ).order_by(Message.timestamp.desc()).first()
        friend = {
            'id': friendship.friend_id,
            'nickname': friendship.friend.nickname,
            'phone': friendship.friend.phone,
            'avatar': f"{request.host_url}{friendship.friend.avatar}" if friendship.friend.avatar else f"{request.host_url}static/default/default_avatar.png",
            'bio': friendship.friend.bio,
            'is_admin': friendship.friend.is_admin,
            'is_forbidden': friendship.friend.is_forbidden,
            'auth_status': friendship.friend.auth_status,
            'created_at': str(friendship.created_at),
            'last_message': last_message.to_dict() if last_message else None,
            'unread_count': unread_counts.get(str(friendship.friend_id), 0)
        }
        friends.append(friend)

    # Filter friends if a search query is provided
    if search_query:
        search_query_lower = search_query.lower()
        friends = [
            friend for friend in friends
            if search_query_lower in friend['nickname'].lower() or
               search_query_lower in friend['phone']
        ]

    return jsonify(friends), 200


@friend_bp.route('/find_user/phone', methods=['POST'])
@jwt_required()
def find_user_by_phone():
    """
    Find a user by their phone number.
    Request body (JSON):
        {
            "phone": "123456"
        }
    """
    # 获取当前用户ID
    user_id = json.loads(get_jwt_identity()).get('id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # 获取请求体中的手机号
    data = request.get_json()
    if not data or 'phone' not in data:
        return jsonify({'error': 'Phone number is required'}), 400

    phone = data['phone'].strip()
    if not phone:
        return jsonify({'error': 'Phone number is required'}), 400

    # 在数据库中查找用户
    user = User.query.filter_by(phone=phone,is_admin = False).first()
    if user.id == user_id:
        return jsonify({'error': 'You cannot add yourself as a friend'}), 404
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.avatar:
        avatar_url = f"{request.host_url}{user.avatar}"
    else:
        avatar_url = f"{request.host_url}static/default/default_avatar.png"

    # 返回用户详细信息
    return jsonify({
        'id': user.id,
        'nickname': user.nickname,
        'phone': user.phone,
        'avatar': avatar_url,
        'bio': user.bio,
        'is_admin': user.is_admin,
        'is_forbidden': user.is_forbidden,
        'auth_status': user.auth_status
    }), 200


@friend_bp.route('/find_user', methods=['POST'])
@jwt_required()
def find_user_by_id():
    """
    Find a user by their user ID and check if they are friends with the current user.
    Request body (JSON):
        {
            "user_id": 2
        }
    """
    # 获取当前用户ID
    current_user_id = json.loads(get_jwt_identity()).get('id')
    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # 获取请求体中的用户ID
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'error': 'User ID is required'}), 400

    target_user_id = int(data['user_id'])
    if not target_user_id or not isinstance(target_user_id, int):
        return jsonify({'error': 'Invalid User ID'}), 400

    # 在数据库中查找用户
    user = User.query.filter_by(id=target_user_id, is_admin=False).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # 判断是否为好友
    friendship = Friendship.query.filter_by(user_id=current_user_id, friend_id=target_user_id).first()
    is_friend = friendship is not None

    if user.avatar:
        avatar_url = f"{request.host_url}{user.avatar}"
    else:
        avatar_url = f"{request.host_url}static/default/default_avatar.png"
    
    # 查找用户状态
    user_status = Status.query.filter_by(user_id=target_user_id, is_active=True).first()
    
    # 返回用户详细信息及好友关系状态
    return jsonify({
        'id': user.id,
        'nickname': user.nickname,
        'phone': user.phone,
        'avatar': avatar_url,
        'bio': user.bio,
        'is_admin': user.is_admin,
        'is_forbidden': user.is_forbidden,
        'auth_status': user.auth_status,
        'is_friend': is_friend,  # 是否是好友
        'status': user_status.to_dict() if user_status else None,  # 用户状态
    }), 200


@friend_bp.route('/friends/check', methods=['GET'])
@jwt_required()
def check_friendship():
    """Check if a user is already a friend."""
    user_id = json.loads(get_jwt_identity()).get('id')
    friend_id = request.args.get('friend_id', type=int)

    if not friend_id:
        return jsonify({'error': 'Friend ID is required'}), 400

    # Check friendship status
    friendship = Friendship.query.filter_by(user_id=user_id, friend_id=friend_id).first()
    return jsonify({'isFriend': friendship is not None}), 200
