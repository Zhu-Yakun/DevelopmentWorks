from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Status, db
from datetime import datetime, timezone
import json

status_bp = Blueprint('status', __name__)

@status_bp.route('/create', methods=['POST'])
@jwt_required()
def create_status():
    """创建新状态."""
    data = request.json
    user_id = json.loads(get_jwt_identity())['id']
    # 查找用户的活动状态
    status = Status.query.filter_by(user_id=user_id, is_active=True).all()
    # 结束用户的所有活动状态
    for s in status:
        s.is_active = False
    if status:
        db.session.commit()

    status_id = data.get('status_id')
    content = data.get('content')

    # 创建新状态
    new_status = Status(
        user_id=user_id,
        status_id=status_id,
        content=content,
        created_at=datetime.now(timezone.utc),
        is_active=True
    )
    db.session.add(new_status)
    db.session.commit()

    return jsonify({"message": "状态创建成功", "status": new_status.to_dict()}), 201

@status_bp.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_status(id):
    """修改当前活动状态."""
    data = request.json
    user_id = json.loads(get_jwt_identity())['id']
    status_id = int(data.get('status_id'))
    # print(status_id)
    content = data.get('content')

    # 查找用户的活动状态
    status = Status.query.filter_by(id=id, user_id=user_id, is_active=True).first()
    if not status:
        return jsonify({"message": "找不到活动状态或状态已结束"}), 404

    # 更新状态内容
    status.status_id = status_id
    status.content = content
    db.session.commit()

    return jsonify({"message": "状态更新成功", "status": status.to_dict()}), 200

@status_bp.route('/end/<int:id>', methods=['POST'])
@jwt_required()
def end_status(id):
    """结束活动状态."""
    user_id = json.loads(get_jwt_identity())['id']

    # 查找用户的活动状态
    status = Status.query.filter_by(id=id, user_id=user_id, is_active=True).first()
    if not status:
        return jsonify({"message": "找不到活动状态或状态已结束"}), 404

    # 将状态标记为已结束
    status.is_active = False
    db.session.commit()

    return jsonify({"message": "状态已结束", "status": status.to_dict()}), 200

@status_bp.route('/history', methods=['GET'])
@jwt_required()
def view_history():
    """查看所有历史状态."""
    user_id = json.loads(get_jwt_identity())['id']

    # 获取所有状态
    statuses = Status.query.filter_by(user_id=user_id).order_by(Status.created_at.desc()).all()
    result = [status.to_dict() for status in statuses]

    return jsonify(result), 200

@status_bp.route('/active', methods=['GET'])
@jwt_required()
def active():
    """查看用户是否有当前活动状态."""
    user_id = json.loads(get_jwt_identity())['id']

    # 查找用户是否有当前活动状态
    status = Status.query.filter_by(user_id=user_id, is_active=True).first()
    if not status:
        return jsonify({"has_status": False}), 200

    return jsonify({"has_status": True, "status": status.to_dict()}), 200

@status_bp.route('/getstatus', methods=['GET'])
@jwt_required()
def get_status():
    """查看用户当前状态."""
    user_id = json.loads(get_jwt_identity())['id']

    # 查找用户当前活动状态
    status = Status.query.filter_by(user_id=user_id, is_active=True).first()
    if not status:
        return jsonify({"message": "当前没有活动状态"}), 404

    return jsonify({"status": status.to_dict()}), 200
