from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from models import db, SystemNotification  # 假设 models.py 定义了数据库表
from sqlalchemy.exc import SQLAlchemyError
import json

# 创建蓝图
system_notification_bp = Blueprint('/system_notification', __name__)

# @system_notification_bp.route('/notifications', methods=['POST'])
# def create_notification():
#     """创建新的系统消息."""
#     try:
#         data = request.json
#         new_notification = SystemNotification(
#             title=data['title'],
#             content=data['content'],
#             user_id=data.get('user_id'),  # 可选字段
#             type=data['type']
#         )
#         db.session.add(new_notification)
#         db.session.commit()
#         return jsonify({'message': 'Notification created successfully', 'notification': new_notification.to_dict()}), 201
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 400
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({'error': 'Database error'}), 500


def create_system_message(title, content, user_id, type):
    new_message = SystemNotification(
        title=title,
        content=content,
        user_id=user_id,
        type=type,
        created_at=datetime.now(timezone.utc),
        is_read=False
    )
    db.session.add(new_message)
    db.session.commit()


@system_notification_bp.route('/get_latest_notification_by_user_id', methods=['GET'])
@jwt_required()
def get_latest_notification_by_user_id():
    """获取指定用户的最新系统消息."""
    id = json.loads(get_jwt_identity())['id']
    try:
        notification1 = SystemNotification.query.filter_by(user_id=id).order_by(SystemNotification.created_at.desc()).first()
        notification2 = SystemNotification.query.filter(SystemNotification.user_id == None).order_by(SystemNotification.created_at.desc()).first()
        if notification1 and notification2:
            notification = notification1 if notification1.created_at > notification2.created_at else notification2
        else:
            notification = notification1 or notification2
        if not notification:
            return jsonify({'message': 'No notifications found'}), 200
        return jsonify({'notification': notification.to_simple_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/get_all_notification_by_user_id', methods=['GET'])
@jwt_required()
def get_all_notification_by_user_id():
    """获取所有系统消息，暂不支持分页."""
    id = json.loads(get_jwt_identity())['id']
    try:
        notifications = SystemNotification.query.filter_by(user_id=id or None).order_by(SystemNotification.created_at.desc()).all()
        return jsonify({
            'notifications': [notification.to_dict() for notification in notifications],
            'total': len(notifications),
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/get_unread_notifications_count', methods=['GET'])
@jwt_required()
def get_unread_notifications_count():
    """获取指定用户的未读消息数量."""
    id = json.loads(get_jwt_identity())['id']
    try:
        unread_num = SystemNotification.query.filter_by(user_id=id or None, is_read=False).count()
        return jsonify({'unread_num': unread_num}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_notification_bp.route('/update_system_notification_status/<int:id>', methods=['PUT'])
@jwt_required()
def update_notification(id):
    """更新指定ID的系统消息已读装态"""
    notification = SystemNotification.query.get(id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    try:
        notification.is_read = True
        db.session.commit()
        return jsonify({'message': 'Notification updated successfully', 'notification': notification.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/update_all_system_notification_status', methods=['PUT'])
@jwt_required()
def update_all_notification():
    """更新所有系统消息的已读状态."""
    id = json.loads(get_jwt_identity())['id']
    try:
        notifications = SystemNotification.query.filter_by(user_id=id).all()
        for notification in notifications:
            notification.is_read = True
        db.session.commit()
        return jsonify({'message': 'All notifications updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_notification_bp.route('/delete_system_notification/<int:id>', methods=['DELETE'])
def delete_notification(id):
    """删除指定ID的系统消息."""
    notification = SystemNotification.query.get(id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    try:
        db.session.delete(notification)
        db.session.commit()
        return jsonify({'message': 'Notification deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# def init_():
#     create_system_message('系统消息', '欢迎使用本系统', None, 'User Ban')
#     create_system_message('系统消息', '欢迎使用本系统', 1, 'Real-Name Authentication')
#     create_system_message('系统消息', '欢迎使用本系统', 2, 'System Broadcast')
