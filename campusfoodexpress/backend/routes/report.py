import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Report, db
from datetime import datetime, timezone
from utils import upload_images
from decorators import admin_required
from routes.system_notification import create_system_message
from sqlalchemy.exc import SQLAlchemyError
import json

report_bp = Blueprint('report', __name__)


"""--------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------  用户路由  --------------------------------------------------"""
"""--------------------------------------------------------------------------------------------------------"""
@report_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_report():
    """用户提交举报."""
    data = request.form
    user_id = json.loads(get_jwt_identity())['id']
    text = data.get('text')
    report_image = request.files.get('image')

    # 检查并保存举报图片
    if report_image:
        image_path = upload_images(report_image, user_id, upload_type="reports")
        if not image_path:
            return jsonify({"message": "图片上传失败"}), 400
    else:
        image_path = None

    # 创建举报
    report = Report(
        user_id=user_id,
        text=text,
        image_path=image_path
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({"message": "举报提交成功"}), 201


"""--------------------------------------------------------------------------------------------------------"""
"""------------------------------------------- 管理员路由 --------------------------------------------------"""
"""--------------------------------------------------------------------------------------------------------"""
@report_bp.route('/all', methods=['GET'])
@admin_required
def view_all_reports():
    """管理员查看所有举报."""
    user_id = json.loads(get_jwt_identity())['id']
    admin_user = User.query.get(user_id)

    # 确认管理员权限
    if not admin_user.is_admin:
        return jsonify({"message": "无权限查看举报"}), 403

    # 获取所有举报
    reports = Report.query.order_by(Report.created_at.desc()).all()
    result = [
        {
            "id": report.id,
            "user_id": report.user_id,
            "text": report.text,
            "image_path": f"{request.host_url}{report.image_path}",
            "status": report.status,
            "created_at": str(report.created_at),
            "review_date": str(report.review_date) if report.review_date else None,
            "reviewed_by": report.reviewed_by
        }
        for report in reports
    ]

    return jsonify(result), 200

@report_bp.route('/review/<int:report_id>', methods=['POST'])
@admin_required
def review_report(report_id):
    """管理员处理举报."""
    try:
        data = request.json
        status = data.get('status')
        user_id = json.loads(get_jwt_identity())['id']

        # 确认管理员权限
        admin_user = User.query.get(user_id)
        if not admin_user.is_admin:
            return jsonify({"message": "无权限处理举报"}), 403

        # 获取举报并更新状态
        report = Report.query.get(report_id)
        if not report:
            return jsonify({"message": "找不到举报"}), 404

        # 更新举报状态和处理时间
        report.status = status
        report.review_date = datetime.now(timezone.utc)
        report.reviewed_by = user_id

        # 创建系统通知，通知被举报的用户
        create_system_message(
            title="举报处理通知",
            content=f"您的举报（举报ID：{report_id}）已被管理员处理，状态：{status}。",
            user_id=report.user_id,
            type="Report Handling"
        )

        # 提交更改
        db.session.commit()

        return jsonify({"message": "举报已处理"}), 200

    except SQLAlchemyError as e:
        # 如果发生数据库错误，进行回滚
        db.session.rollback()
        print(f"数据库错误: {e}")
        return jsonify({"message": "数据库错误，处理失败"}), 500

    except Exception as e:
        # 捕获其他异常并回滚
        db.session.rollback()
        print(f"发生错误: {e}")
        return jsonify({"message": "处理过程中发生错误"}), 500