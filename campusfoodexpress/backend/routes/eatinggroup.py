

# Restaurant backend implementation
from flask import Blueprint, request, jsonify, current_app
from models import EatingGroup, EatingGroupMember, User, db, Message
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import upload_images
from decorators import admin_required
from .chat import get_group_unread_count
from datetime import datetime
import json

eatinggroup_bp = Blueprint('eatinggroup', __name__)

def add_each_member(group_id, user_id):
    new_member = EatingGroupMember(
        user_id=user_id,
        role='member',
        group_id=group_id,
    )
    db.session.add(new_member)
    return new_member

# EatingGroup
# 创建群聊
@eatinggroup_bp.route('/add_group', methods=['POST'])
@jwt_required()
def add_group():
    data = request.get_json()
    user_id = json.loads(get_jwt_identity()).get('id')
    member_user_ids = data.get('member_user_ids')
    try:
        new_group = EatingGroup(
            name=data.get('name'),
            description=data.get('description'),
            latest_message_id=None,
            owner_user_id=user_id,
            image = f"{request.host_url}static/default/group_avatar.png"
        )
        db.session.add(new_group)
        db.session.flush()
        owner = EatingGroupMember(
            user_id=user_id,
            role='owner',
            group_id=new_group.id
        )
        db.session.add(owner)
        for member_user_id in member_user_ids:
            add_each_member(new_group.id, member_user_id)
        db.session.commit()
        return jsonify({'message': 'Group added successfully', 'group': new_group.to_dict(), 'owner':owner.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# user_id获取群聊
@eatinggroup_bp.route('/get_group_by_userid', methods=['GET'])
@jwt_required()
def get_group_by_memberid():
    user_id = json.loads(get_jwt_identity()).get('id')
    groups = EatingGroup.query.join(EatingGroupMember).filter(EatingGroupMember.user_id == user_id).all()
    groups.sort(key=lambda x: x.latest_message_id if x.latest_message_id else -1, reverse=True)
    unread_counts = get_group_unread_count(user_id)
    groups_list = []
    for group in groups:
        if group.latest_message_id:
            message = Message.query.filter_by(id=group.latest_message_id).first()
            last_message = message.to_dict()

        else:
            last_message = None
        group_msg = {
                **group.to_dict_without_messages(),  # 原有字段
                'last_message': last_message,  # 新增 latest_message 字段
                'unread_count': unread_counts.get(group.id, 0)  # 新增 unread_count 字段
            }
        groups_list.append(group_msg)
    return jsonify({'groups': groups_list})

@eatinggroup_bp.route('/get_all_group', methods=['GET'])
@jwt_required()
def get_all_groups():
    groups = EatingGroup.query.all()
    return jsonify({'groups': [group.to_dict() for group in groups]})

# 根据group_id获取群聊信息
@eatinggroup_bp.route('/get_group_by_groupid', methods=['GET'])
@jwt_required()
def get_group_by_id():
    group_id = request.args.get('group_id')
    group = EatingGroup.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    return jsonify({'group': group.to_dict_without_messages()}), 200

# 更新群聊
@eatinggroup_bp.route('/update_group', methods=['POST'])
@jwt_required()
def update_group():
    data = request.get_json()
    try:
        group = EatingGroup.query.get(data.get('id'))
        if not group:
            return jsonify({'error': 'Group not found'}), 404
        if data.get('image'):
            group.image = data.get('image')
        if data.get('name'):
            group.name = data.get('name')
        if data.get('description'):
            group.description = data.get('description')
        db.session.commit()
        return jsonify({'message': 'Group updated successfully', 'group': group.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 删除群聊
@eatinggroup_bp.route('/delete_group', methods=['DELETE'])
@jwt_required()
def delete_group():
    group_id = request.args.get('group_id')
    group = EatingGroup.query.get(group_id)
    if not group:
        return jsonify({'error': 'Group not found'}), 404

    # Delete all members of the group
    for member in group.members:
        db.session.delete(member)
    
    # Delete all messages of the group
    # for message in group.messages:
    #     db.session.delete(message)

    db.session.delete(group)
    db.session.commit()
    return jsonify({'message': 'Group and its members and messages deleted successfully'}), 200

# EatingGroupMember
# 添加群成员
@eatinggroup_bp.route('/add_member', methods=['POST'])
@jwt_required()
def add_member():
    data = request.get_json()
    try:
        if not EatingGroup.query.get(data.get('group_id')):
            return jsonify({'error': 'Group not found'}), 404
        if not User.query.get(data.get('user_id')):
            return jsonify({'error': 'User not found'}), 404
        if EatingGroupMember.query.filter_by(user_id=data.get('user_id'), group_id=data.get('group_id')).first():
            return jsonify({'error': 'Member already exists'}), 400
        new_member=add_each_member(data.get('group_id'), data.get('user_id'))
        db.session.commit()
        return jsonify({'message': 'Member added successfully', 'member': new_member.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# 获取群成员
@eatinggroup_bp.route('/get_members', methods=['GET'])
@jwt_required()
def get_members():
    try:
        group_id = request.args.get('group_id')
        print(group_id)
        members = EatingGroup.query.get(group_id).members
        return jsonify({'members': [member.to_dict() for member in members]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# # 转移群主 new_owner_id, group_id
# @eatinggroup_bp.route('/update_owner', methods=['POST'])
# @jwt_required()
# def update_owner():
#     data = request.get_json()
#     try:
#         old_owner = next((member for member in EatingGroup.query.get(data.get('group_id')).members if member.role == 'owner'), None)
#         # if not old_owner:
#             # return jsonify({'error': 'Group has no owner'}), 400
#         new_owner = EatingGroupMember.query.get(data.get('new_owner_id'))
#         if not new_owner:
#             return jsonify({'error': 'New owner not found'}), 404
#         if new_owner.group_id != data.get('group_id'):
#             return jsonify({'error': 'New owner is not a member of the group'}), 400
#         if old_owner:
#             old_owner.role = 'member'
#         new_owner.role = 'owner'
#         db.session.commit()
#         return jsonify({'message': 'Owner updated successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# 删除群成员
@eatinggroup_bp.route('/delete_member_by_memberid', methods=['DELETE'])
@jwt_required()
def delete_member():
    data = request.get_json()
    print(data)
    try:
        member = EatingGroupMember.query.get(data.get('id'))
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        if member.role == 'owner':
            return jsonify({'error': 'Owner cannot be deleted'}), 400
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400
