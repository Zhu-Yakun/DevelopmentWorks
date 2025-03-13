from flask import Blueprint, jsonify, request
from extensions import db
from models import Favorite, User, Restaurant
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
favorite_bp = Blueprint('favorite', __name__)

@favorite_bp.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    if request.method == 'OPTIONS':
        # 直接返回 200 响应
        return jsonify({}), 200
    
    """添加收藏餐馆"""
    user_id = json.loads(get_jwt_identity()).get('id')
    restaurant_id = request.json.get('restaurant_id')
    
    # 检查餐馆是否存在
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}), 404
    
    # 检查是否已经收藏过
    existing_favorite = Favorite.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).first()
    if existing_favorite:
        return jsonify({'error': 'Already favorited'}), 400
    
    # 添加收藏
    new_favorite = Favorite(user_id=user_id, restaurant_id=restaurant_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite added successfully'}), 201

@favorite_bp.route('/favorites/<int:restaurant_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(restaurant_id):
    """删除收藏餐馆"""
    user_id = json.loads(get_jwt_identity()).get('id')
    
    # 检查收藏是否存在
    favorite = Favorite.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).first()
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    # 删除收藏
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Favorite deleted successfully'}), 200

@favorite_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """获取用户收藏的餐馆列表"""
    user_id = json.loads(get_jwt_identity()).get('id')
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    # 返回收藏的餐馆信息
    favorite_restaurants = [
        {
            'id': favorite.restaurant.id,
            'name': favorite.restaurant.name,
            'address': favorite.restaurant.address,
            'phone': favorite.restaurant.phone,
            'image': f"{request.host_url}{favorite.restaurant.image}",
            'created_at': favorite.created_at
        }
        for favorite in favorites
    ]
    
    return jsonify(favorite_restaurants), 200

@favorite_bp.route('/favorites/check', methods=['GET'])
@jwt_required()
def check_favorite():
    """检查是否收藏某餐馆"""
    user_id = json.loads(get_jwt_identity()).get('id')
    restaurant_id = request.args.get('restaurant_id', type=int)

    if not restaurant_id:
        return jsonify({'error': 'Restaurant ID is required'}), 400

    # 检查收藏状态
    favorite = Favorite.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).first()
    return jsonify({'isFavorited': favorite is not None}), 200
