from flask import Blueprint, jsonify, request, session
from extensions import socketio
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from flask_socketio import emit, join_room, leave_room
from models import db, Message,  EatingGroupMember,EatingGroup,Friendship
from sqlalchemy import func
import datetime
import json

chat_bp = Blueprint('chat', __name__)

def verify_jwt_token(token):
    try:
        # 解码 JWT token
        decoded_token = decode_token(token)
        return decoded_token
    except Exception as e:
        return None
    
@socketio.on('join_room')
def handle_connect(auth):
    if not auth:
        print(f"Client disconnected: {request.sid} - No auth data provided")
        return False  # 拒绝连接
    
    token = auth.get('token')
    if not token:
        print(f"Client disconnected: {request.sid} - No token provided")
        return False  # 拒绝连接
    
    user = verify_jwt_token(token)
    print(user)
    if not user:
        print(f"Client disconnected: {request.sid} - Invalid token")
        return False  # 拒绝连接
    
    user_id = json.loads(user['sub'])["id"]  # 获取当前用户的 ID
    join_room(f"user_{user_id}")  # 加入用户的个人房间
    print(f"User {user_id} connected")
    
    # 获取用户的群组列表
    user_groups = EatingGroupMember.query.filter_by(user_id=user_id).all()
    for group_member in user_groups:
        print(group_member.group_id)
        join_room(f"group_{group_member.group_id}")  # 加入该群组的房间
        print(f"User {user_id} joined group {group_member.group_id}")

@socketio.on('leave_room')
def handle_disconnect(auth):
    if not auth:
        print(f"Client disconnected: {request.sid} - No auth data provided")
        return False  # 拒绝连接
    
    token = auth.get('token')
    if not token:
        print(f"Client disconnected: {request.sid} - No token provided")
        return False  # 拒绝连接
    
    user = verify_jwt_token(token)
    print(user)
    if not user:
        print(f"Client disconnected: {request.sid} - Invalid token")
        return False  # 拒绝连接
    
    user_id = json.loads(user['sub'])["id"]  # 获取当前用户的 ID
    leave_room(f"user_{user_id}")  # 离开用户的个人房间
    print(f"User {user_id} disconnected")
    
    # 获取用户的群组列表
    user_groups = EatingGroupMember.query.filter_by(user_id=user_id).all()
    for group_member in user_groups:
        leave_room(f"group_{group_member.group_id}")  # 离开群组的房间
        print(f"User {user_id} left group {group_member.group_id}")


# 处理私聊消息
@socketio.on('private_message')
def handle_private_message(data):
    """处理私聊消息"""
    token = data['token']
    if not token:
        return False
    user = verify_jwt_token(token)
    if not user:
        return False
    sender_id = json.loads(user['sub'])["id"]  # 获取当前用户的 ID
    receiver_id = data['message']['receiver_id']  # 获取接收者的ID
    content = data['message']['content']  # 消息内容
    content_type = data['message']['content_type'] # 获取消息类型
    time = datetime.datetime.now()
    # 保存消息到数据库
    message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, content_type=content_type, timestamp=time)
    db.session.add(message)
    db.session.commit()# 如遇性能瓶颈，可能需要事物处理优化 TODO
    print(str(data['message']))
    # 更新发送者的最后阅读时间
    friendship = Friendship.query.filter_by(user_id=sender_id, friend_id=receiver_id).first()
    if friendship:
        friendship.last_read_time = time
        db.session.commit()
    # 广播消息给接收者
    emit('private_message', message.to_dict(), room=f'user_{receiver_id}')



# 处理群聊消息
@socketio.on('group_message')
def handle_group_message(data):
    """处理群聊消息"""
    token = data['token']
    if not token:
        return False
    user = verify_jwt_token(token)
    if not user:
        return False
    sender_id = json.loads(user['sub'])["id"] # 获取当前用户的 ID
    group_id = data['message']['group_id']  # 获取群组ID
    content = data['message']['content']  # 消息内容
    content_type = data['message']['content_type'] # 获取消息类型
    # 保存消息到数据库
    message = Message(sender_id=sender_id, group_id=group_id, content=content, content_type=content_type, timestamp=datetime.datetime.now())
    db.session.add(message)
    db.session.commit()# 如遇性能瓶颈，可能需要事物处理优化 TODO
    # 更新群组的最新消息ID和发送者的最后阅读时间
    group = EatingGroup.query.filter_by(id=group_id).first()
    group.latest_message_id = message.id
    member = EatingGroupMember.query.filter_by(user_id=sender_id, group_id=group_id).first()
    member.last_read_time = datetime.datetime.now()
    db.session.commit()
    # 广播消息到群组
    emit('group_message', message.to_dict(), room=f'group_{group_id}')


def get_unread_count(receiver_id):#data

    friendships = Friendship.query.filter_by(user_id=receiver_id).all()
    unread_counts = {}
    for friendship in friendships:
        if friendship.last_read_time:
            unread_count = Message.query.filter(
                Message.sender_id == friendship.friend_id,
                Message.receiver_id == receiver_id,
                Message.timestamp > friendship.last_read_time
            ).count()
        else:
            # 如果没有最后阅读时间，认为该好友的所有消息都是未读
            unread_count = Message.query.filter(
                Message.sender_id == friendship.friend_id,
                Message.receiver_id == receiver_id
            ).count()
        unread_counts[str(friendship.friend_id)] = unread_count
    return unread_counts



# 将私聊消息标记为已读
@socketio.on('private_read')
def mark_read(data):
    token = data['token']
    if not token:
        return False
    user = verify_jwt_token(token)
    if not user:
        return False
    receiver_id = json.loads(user['sub'])["id"]
    sender_id = data['sender_id']  # 获取接收者的ID
    if not receiver_id or not sender_id:
        emit('private_read', {'error': 'Missing receiver_id or sender_id'}, room=f'user_{receiver_id}')
    friendship = Friendship.query.filter_by(user_id=receiver_id, friend_id=sender_id).first()
    if friendship:
        friendship.last_read_time = datetime.datetime.now()
        db.session.commit()
    emit('private_read', {'message': 'Messages marked as read'}, room=f'user_{receiver_id}')


def get_group_unread_count(user_id):#data
    # 获取用户所有的群组
    user_groups = EatingGroupMember.query.filter_by(user_id=user_id).all()  
    unread_counts = {}  # 用于存储每个群组的未读消息数量
    # 遍历所有群组，计算每个群组的未读消息数量
    for group_member in user_groups:
        group_id = group_member.group_id
        
        if group_member.last_read_time:
            unread_count = Message.query.filter(
                Message.group_id == group_id,
                Message.timestamp > group_member.last_read_time
            ).count()
        else:
            # 如果没有最后阅读时间，认为该成员的所有消息都是未读
            unread_count = Message.query.filter(
                Message.group_id == group_id
            ).count()

        unread_counts[group_id] = unread_count  # 将群组的未读消息数量保存到字典
    return unread_counts

    
# 将群聊消息标记为已读
@socketio.on('group_read')
def mark_group_read(data):
    token = data['token']
    if not token:
        return False
    user = verify_jwt_token(token)
    if not user:
        return False
    user_id = json.loads(user['sub'])["id"]  # 获取当前用户的 ID
    group_id = data['group_id']  # 获取群组ID
    if not group_id:
        return jsonify({"error": "Missing group_id"}), 400
    # 查询成员
    member = EatingGroupMember.query.filter_by(user_id=user_id, group_id=group_id).first()
    if member:
        # 更新成员的最后阅读时间
        member.last_read_time = datetime.datetime.now()
        db.session.commit()
        emit('group_read', {'message': 'Messages marked as read'}, room=f'user_{user_id}')
    else:
        emit('group_read', {'error': 'Member not found'}, room=f'user_{user_id}')

# 获取消息历史（分页）
@chat_bp.route('/get_history', methods=['GET'])
@jwt_required()  # 确保请求必须携带有效的 JWT token
def get_message_history():
    current_user_id = json.loads(get_jwt_identity())["id"]  # 获取当前用户的身份
    receiver_id = request.args.get('receiver_id')  # 获取接收者的 ID（私聊时用）
    group_id = request.args.get('group_id')  # 获取群 ID（群聊时用）
    page = request.args.get('page', 1, type=int)  # 当前页码，默认为1
    per_page = request.args.get('per_page', 20, type=int)  # 每页的消息数，默认为20

    if not receiver_id and not group_id:
        return jsonify({"error": "Missing receiver_id or group_id"}), 400

    # 根据接收者 ID 查询历史消息（私聊）
    if receiver_id:
        messages_query = Message.query.filter(
            ((Message.sender_id == current_user_id) & (Message.receiver_id == receiver_id)) |
            ((Message.sender_id == receiver_id) & (Message.receiver_id == current_user_id))
        )
    # 根据群 ID 查询历史消息（群聊）
    elif group_id:
        messages_query = Message.query.filter_by(group_id=group_id)

    # 分页查询历史消息，按时间降序排列（最新消息在最上面）
    messages = messages_query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)

    # 将消息转换为字典格式并返回
    return jsonify({
        'messages': [message.to_dict() for message in messages.items],
        'has_next': messages.has_next,  # 是否还有下一页
        'has_prev': messages.has_prev,  # 是否有上一页
        'next_num': messages.next_num,  # 下一页页码
        'prev_num': messages.prev_num,  # 上一页页码
    })

