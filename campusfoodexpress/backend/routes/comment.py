# Comment backend implementation for Restaurant System
from flask import Blueprint, request, jsonify, current_app
from models import Comment, db, Restaurant, Order
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from utils import upload_images
from decorators import admin_required
import os
import json
from routes.system_notification import create_system_message
from sqlalchemy.exc import SQLAlchemyError
from routes.order_notification import create_order_notification

comment_bp = Blueprint('comment', __name__)

"""--------------------------------------------------------------------------------------------------------"""
"""------------------------------------------- 管理员路由 --------------------------------------------------"""
"""--------------------------------------------------------------------------------------------------------"""
@comment_bp.route('/delete/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """管理员删除评论并发送通知."""
    try:
        # 获取评论对象，如果不存在则抛出404异常
        comment = Comment.query.get_or_404(comment_id)

        # 获取评论作者的用户ID
        user_id = comment.user_id
        order_id = comment.order_id
        order = Order.query.get(order_id)
        order.comment_id = None

        # 删除评论相关的图片（如果存在）
        if comment.images:
            for image_path in comment.images.split(";"):
                if os.path.exists(image_path):
                    os.remove(image_path)

        # 删除评论
        db.session.delete(comment)

        # 创建系统通知，通知被删除评论的用户
        create_system_message(
            title="评论删除通知",
            content=f"您的评论（评论ID：{comment_id}）已被删除。",
            user_id=user_id,
            type="Others"
        )

        # 提交事务
        db.session.commit()

        # 返回成功消息
        return jsonify({'message': 'Comment deleted successfully'}), 200

    except SQLAlchemyError as e:
        # 捕获数据库错误，回滚事务
        db.session.rollback()
        print(f"数据库错误: {e}")
        return jsonify({'error': '数据库错误，删除失败'}), 500

    except Exception as e:
        # 捕获其他异常，回滚事务
        db.session.rollback()
        print(f"发生错误: {e}")
        return jsonify({'error': f'发生错误: {str(e)}'}), 500

"""--------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------- 用户路由 ---------------------------------------------------"""
"""--------------------------------------------------------------------------------------------------------"""
# Add a new comment with optional images
@comment_bp.route('/add', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.form
    user_data = get_jwt_identity()
    user_data = json.loads(user_data)
    # 处理 rating 类型问题，确保是整数
    try:
        rating = int(data['rating'])  # 将 rating 转换为整数
    except ValueError:
        return jsonify({'error': 'Invalid rating value'}), 400

    # Save image if provided
    image_paths = []
    if 'images' in request.files:
        files = request.files.getlist('images')
        for file in files:
            image_url = upload_images(file, user_data['id'], upload_type="comments")
            if image_url:
                image_paths.append(image_url)
            else:
                return jsonify({'error': '图片上传失败'}), 400
    # Create new comment
    new_comment = Comment(
        user_id=user_data['id'],
        order_id=data.get('order_id'),
        restaurant_id=data['restaurant_id'],
        text=data['text'],
        rating=rating,  # 使用转换后的整数类型
        created_at=datetime.now(timezone.utc),
        images=";".join(image_paths) if image_paths else None,
        is_anonymous = data.get('is_anonymous', 'false').lower() == 'true'
    )

    try:
        order = Order.query.get(data['order_id'])
        if order is None:
            return jsonify({'error': 'Order not found'}), 404
        if order.comment_id is not None:
            return jsonify({'error': 'Comment already exists for this order'}), 400
        db.session.add(new_comment)
        db.session.commit()
        order.comment_id = new_comment.id
        create_order_notification('评论已发布', '您的评论已发布，感谢您的支持。', user_data['id'], data['order_id'], 'Order Commented')
        db.session.commit()

        return jsonify({'message': 'Comment added successfully', 'image_urls': image_paths}), 201

    except Exception as e:
        # 如果发生异常，回滚事务
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get comments by restaurant ID
@comment_bp.route('/get_by_restaurant/<int:restaurant_id>', methods=['GET'])
@jwt_required()
def get_comments_by_restaurant(restaurant_id):
    try:
        comments = Comment.query.filter_by(restaurant_id=restaurant_id).all()
        comment_data = []
        for comment in comments:
            data = comment.to_dict()
            if comment.images:
                data['images'] = [f"{request.host_url}{img}" for img in comment.images.split(";")]
            comment_data.append(data)
        return jsonify(comment_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Get comments by user ID
@comment_bp.route('/get_by_user/', methods=['GET'])
@jwt_required()
def get_comments_by_user():
    try:
        # 获取当前用户 ID
        user_id = json.loads(get_jwt_identity())['id']
        
        # 查询评论和关联的餐馆信息
        comments = db.session.query(
            Comment.id,
            Comment.rating,
            Comment.created_at,
            Restaurant.name.label('restaurant_name')
        ).join(Restaurant, Comment.restaurant_id == Restaurant.id).filter(Comment.user_id == user_id).all()
        
        # 构造返回数据
        comment_data = [
            {
                'id': comment.id,
                'restaurant_name': comment.restaurant_name,
                'rating': comment.rating,
                'created_at': comment.created_at.isoformat()
            }
            for comment in comments
        ]
        return jsonify(comment_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# get detail of a comment
@comment_bp.route('/get_comment/<int:id>', methods=['GET']) 
@jwt_required()
def get_comment(id):
    try:
        comment = Comment.query.get_or_404(id)
        data = comment.to_dict()
        restaurant = Restaurant.query.get(comment.restaurant_id)
        data['restaurant_name'] = restaurant.name
        data['restaurant_image'] = f"{request.host_url}{restaurant.image}"
        data['restaurant_rating'] = restaurant.rating
        if comment.images:
            data['images'] = [f"{request.host_url}{img}" for img in comment.images.split(";")]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@comment_bp.route('/get_all',methods=['GET'])
@jwt_required()
def get_all_comments():
    try:
        comments = Comment.query.all()
        comment_data = []
        for comment in comments:
            data = comment.to_dict()
            if comment.images:
                data['images'] = [f"{request.host_url}{img}" for img in comment.images.split(";")]
            comment_data.append(data)
        return jsonify(comment_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400