import os
import json
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, VerificationRequest, db
from datetime import datetime, timezone
from utils import upload_images
from decorators import admin_required
from routes.system_notification import create_system_message
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth', __name__)

"""--------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------- 用户路由 ---------------------------------------------------"""
"""--------------------------------------------------------------------------------------------------------"""
@auth_bp.route('/request_verification', methods=['POST'])
@jwt_required()
def request_verification():
    """用户提交实名认证请求."""
    data = request.form
    user_id = json.loads(get_jwt_identity())['id']
    real_name = data.get('real_name')
    id_number = data.get('id_number')
    document_image = request.files.get('img')

    # 检查用户是否已有待处理的实名认证请求
    existing_request = VerificationRequest.query.filter_by(user_id=user_id, status='pending').first()
    if existing_request:
        return jsonify({"message": "已有待处理的实名认证请求"}), 400

    # 检查并保存证件图片
    if document_image:
        image_path = upload_images(document_image, user_id, upload_type="auth")
        if not image_path:
            return jsonify({"message": "图片上传失败"}), 400
    else:
        return jsonify({"message": "请上传证件图片"}), 400

    # 创建新的认证请求
    verification_request = VerificationRequest(
        user_id=user_id,
        real_name=real_name,
        id_number=id_number,
        document_image=image_path
    )
    verification_request.status = 'pending'
    user = User.query.get(user_id)
    user.auth_status = verification_request.status
    db.session.add(verification_request)
    db.session.commit()

    return jsonify({"message": "实名认证请求提交成功"}), 201

@auth_bp.route('/verification_status', methods=['GET'])
@jwt_required()
def verification_status():
    """用户查看自己的实名认证状态."""
    user_id = json.loads(get_jwt_identity())['id']
    auth_status = User.query.get(user_id).auth_status
    return jsonify({
        "status": auth_status,
    }), 200


"""--------------------------------------------------------------------------------------------------------"""
"""------------------------------------------- 管理员路由 --------------------------------------------------"""
"""--------------------------------------------------------------------------------------------------------"""

@auth_bp.route('/review_verification/<int:request_id>', methods=['POST'])
@admin_required
def review_verification(request_id):
    """管理员审核实名认证请求."""
    data = request.json
    status = data.get('status')
    
    user_id = json.loads(get_jwt_identity())['id']

    # 确认管理员权限
    admin_user = User.query.get(user_id)
    if not admin_user.is_admin:
        return jsonify({"message": "无权限进行此操作"}), 403

    try:
        # 获取认证请求并更新状态
        verification_request = VerificationRequest.query.get(request_id)
        if not verification_request:
            return jsonify({"message": "找不到实名认证请求"}), 404

        # 更新认证请求状态
        verification_request.status = status
        verification_request.review_date = datetime.now(timezone.utc)
        verification_request.reviewed_by = user_id

        # 更新用户认证状态
        user = User.query.get(verification_request.user_id)
        user.auth_status = status

        # 发送系统通知
        create_system_message(
            title="实名认证审核结果",
            content=f"您的实名认证请求已被{'通过' if status == 'authorized' else '拒绝'}。",
            user_id=verification_request.user_id,
            type="Real-Name Authentication"
        )

        # 提交更改
        db.session.commit()

        return jsonify({"message": "实名认证请求审核成功"}), 200

    except SQLAlchemyError as e:
        # 数据库错误回滚
        db.session.rollback()
        return jsonify({"message": "操作失败，请稍后再试", "error": str(e)}), 500

    except Exception as e:
        # 捕获其他异常并回滚
        db.session.rollback()
        return jsonify({"message": "操作失败", "error": str(e)}), 500


@auth_bp.route('/all_verification_requests', methods=['GET'])
@admin_required
def all_verification_requests():
    """管理员查看所有实名认证请求."""
    user_id = json.loads(get_jwt_identity())['id']
    admin_user = User.query.get(user_id)

    # 确认管理员权限
    if not admin_user.is_admin:
        return jsonify({"message": "无权限查看实名认证请求"}), 403

    # 获取所有实名认证请求
    requests = db.session.query(
        VerificationRequest.id,
        VerificationRequest.user_id,
        User.nickname,
        User.phone,
        VerificationRequest.real_name,
        VerificationRequest.id_number,
        VerificationRequest.status,
        VerificationRequest.request_date,
        VerificationRequest.review_date,
        VerificationRequest.document_image,
        VerificationRequest.reviewed_by
    ).join(User, VerificationRequest.user_id == User.id).order_by(VerificationRequest.request_date.desc()).all()
    result = [
        {
            "id": req.id,
            "user_id": req.user_id,
            "nike_name": req.nickname,
            "phone": req.phone,
            "real_name": req.real_name,
            'school': "同济大学",
            "id_number": req.id_number,
            "status": req.status,
            "request_date": str(req.request_date),
            "review_date": str(req.review_date) if req.review_date else None,
            "auth_image": f"{request.host_url}{req.document_image}",
            "reviewed_by": req.reviewed_by
        }
        for req in requests
    ]

    return jsonify(result), 200