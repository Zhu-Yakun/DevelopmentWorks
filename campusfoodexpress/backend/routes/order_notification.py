from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from models import db, OrderNotification  # 假设 models.py 定义了数据库表
from sqlalchemy.exc import SQLAlchemyError
import json

# 创建蓝图
order_notification_bp = Blueprint('order_notification', __name__)

def create_order_notification(title, content, user_id, order_id, type):
    """创建订单消息的函数."""
    new_notification = OrderNotification(
        title=title,
        content=content,
        user_id=user_id,
        order_id=order_id,
        type=type,
        created_at=datetime.now(timezone.utc),
        is_read=False
    )
    print(new_notification.type)
    db.session.add(new_notification)
    db.session.commit()
    print("Notification created successfully", new_notification.to_dict())

@order_notification_bp.route('/get_latest_notification_by_user_id', methods=['GET'])
@jwt_required()
def get_latest_notification_by_user_id():
    """获取指定用户的最新订单消息."""
    user_id = json.loads(get_jwt_identity())['id']
    try:
        notification = OrderNotification.query.filter_by(user_id=user_id).order_by(OrderNotification.created_at.desc()).first()
        if not notification:
            return jsonify({'message': 'No notifications found'}), 200
        return jsonify({  
            "message": "Notification created successfully",
            'notification': notification.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/get_all_notifications_by_user_id', methods=['GET'])
@jwt_required()
def get_all_notifications_by_user_id():
    """获取所有订单消息，不支持分页."""
    user_id = json.loads(get_jwt_identity())['id']
    try:
        notifications = OrderNotification.query.filter_by(user_id=user_id).order_by(OrderNotification.created_at.desc()).all()
        return jsonify({
            'notifications': [notification.to_dict() for notification in notifications],
            'total': len(notifications),
            # 'page': notifications.page,
            # 'per_page': notifications.per_page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/get_unread_notifications_count', methods=['GET'])
@jwt_required()
def get_unread_notifications_count():
    """获取用户未读订单消息数量."""
    user_id = json.loads(get_jwt_identity())['id']
    try:
        unread_num = OrderNotification.query.filter_by(user_id=user_id, is_read=False).count()
        print(unread_num)
        return jsonify({'unread_num': unread_num}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/update_order_notification_status/<int:id>', methods=['PUT'])
@jwt_required()
def update_notification_status(id):
    """更新指定订单消息的已读状态."""
    notification = OrderNotification.query.get(id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    try:
        notification.is_read = True
        db.session.commit()
        return jsonify({'message': 'Notification status updated successfully', 'notification': notification.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/update_all_order_notifications_status', methods=['PUT'])
@jwt_required()
def update_all_notifications_status():
    """更新所有订单消息的已读状态."""
    user_id = json.loads(get_jwt_identity())['id']
    try:
        notifications = OrderNotification.query.filter_by(user_id=user_id, is_read=False).all()
        for notification in notifications:
            notification.is_read = True
        db.session.commit()
        return jsonify({'message': 'All notifications status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_notification_bp.route('/delete_notification/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_notification(id):
    """删除指定ID的订单消息."""
    notification = OrderNotification.query.get(id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    try:
        db.session.delete(notification)
        db.session.commit()
        return jsonify({'message': 'Notification deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
