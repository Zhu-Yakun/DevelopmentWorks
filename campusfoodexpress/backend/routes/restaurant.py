# Restaurant backend implementation
from flask import Blueprint, request, jsonify, current_app
from models import Restaurant, db, Order, OrderNotification, Comment,Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import upload_images
from decorators import admin_required
import os

restaurant_bp = Blueprint('restaurant', __name__)
"""-----------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------------管理员路由-------------------------------------------------"""
"""-----------------------------------------------------------------------------------------------------------"""
# Create a new restaurant
@restaurant_bp.route('/add', methods=['POST'])
@admin_required
def add_restaurant():
    data = request.form
    try:
        # Save image if provided
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            image_path = upload_images(file, data['id'], upload_type="restaurants")
            if not image_path:
                return jsonify({'error': '图片上传失败'}), 400
        if 'qr_code' in request.files:
            file = request.files['qr_code']
            qr_code_path = upload_images(file, data['id'], upload_type="restaurants")
            if not qr_code_path:
                return jsonify({'error': '图片上传失败'}), 400

        new_restaurant = Restaurant(
            name=data['name'],
            address=data['address'],
            phone=data['phone'],
            qr_code= qr_code_path if 'qr_code' in request.files else None,
            is_forbidden=data.get('is_forbidden', False),
            description=data.get('description', None),
            sales=data.get('sales', 0),
            image=image_path if 'image' in request.files else None,
            lat=data.get('lat',0),
            lng=data.get('lng',0),
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return jsonify({'message': 'Restaurant added successfully',
                "qr_code":f"{request.host_url}{qr_code_path}",
                "image": f"{request.host_url}{image_path}",
                "id": new_restaurant.id,
                "status": "forbid" if new_restaurant.is_forbidden else "normal"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
 # Update a restaurant
@restaurant_bp.route('/update/<int:restaurant_id>', methods=['PUT'])
@admin_required
def update_restaurant(restaurant_id):
    data = request.form
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        restaurant.name = data.get('name', restaurant.name)
        restaurant.address = data.get('address', restaurant.address)
        restaurant.phone = data.get('phone', restaurant.phone)
        restaurant.description = data.get('description', restaurant.description)
        restaurant.sales = data.get('sales', restaurant.sales)
        restaurant.lat = data.get('lat', restaurant.lat)
        restaurant.lng = data.get('lng', restaurant.lng)
        restaurant.is_forbidden = data.get(False if 'status' == 'normal' else True, restaurant.is_forbidden)
        restaurant.rating = data.get('rating', restaurant.rating)

        # Save new image if provided
        if 'image' in request.files:
            file = request.files['image']
            image_path = upload_images(file, restaurant_id, upload_type="restaurants")
            if not image_path:
                return jsonify({'error': '图片上传失败'}), 400
            # Delete old image if it exists
            if restaurant.image and os.path.exists(restaurant.image):
                os.remove(restaurant.image)
            restaurant.image = image_path
        if 'qr_code' in request.files:
            file = request.files['qr_code']
            qr_code_path = upload_images(file, restaurant_id, upload_type="restaurants")
            if not qr_code_path:
                return jsonify({'error': '图片上传失败'}), 400
            # Delete old qr code if it exists
            if restaurant.qr_code and os.path.exists(restaurant.qr_code):
                os.remove(restaurant.qr_code)
            restaurant.qr_code = qr_code_path
        db.session.commit()
        qr_code_path = restaurant.qr_code if restaurant.qr_code else f"{request.host_url}static/default/qr_code_default.png"
        image_path = restaurant.image if restaurant.image else f"{request.host_url}static/default/restaurant_default.png"
        return jsonify({'message': 'Restaurant updated successfully',
                        "qr_code":f"{request.host_url}{qr_code_path}",
                        "image": f"{request.host_url}{image_path}"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Delete a restaurant
@restaurant_bp.route('/delete/<int:restaurant_id>', methods=['DELETE'])
@admin_required
def delete_restaurant(restaurant_id):
    try:
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        # Delete image if it exists
        if restaurant.image and os.path.exists(restaurant.image):
            os.remove(restaurant.image)
            if os.path.exists(os.path.dirname(restaurant.image)):
                for file in os.listdir(os.path.dirname(restaurant.image)):
                    os.remove(os.path.join(os.path.dirname(restaurant.image), file))
                os.rmdir(os.path.dirname(restaurant.image))
        # Delete qr code if it exists
        if restaurant.qr_code and os.path.exists(restaurant.qr_code):
            os.remove(restaurant.qr_code)
            if os.path.exists(os.path.dirname(restaurant.qr_code)):
                for file in os.listdir(os.path.dirname(restaurant.qr_code)):
                    os.remove(os.path.join(os.path.dirname(restaurant.qr_code), file))
                os.rmdir(os.path.dirname(restaurant.qr_code))
        orders=Order.query.filter_by(restaurant_id=restaurant_id)
        comments=Comment.query.filter_by(restaurant_id=restaurant_id)
        favorites=Favorite.query.filter_by(restaurant_id=restaurant_id)
        for order in orders:
            OrderNotification.query.filter_by(order_id=order.id).delete()
            db.session.delete(order)
        for comment in comments:
            db.session.delete(comment)
        for favorite in favorites:
            db.session.delete(favorite)
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({'message': 'Restaurant deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Forbid a restaurant
@restaurant_bp.route('/forbid/<int:id>', methods=['PATCH'])
@admin_required
def forbid_restaurant(id):
    try:
        restaurant = Restaurant.query.get_or_404(id)
        restaurant.is_forbidden = True
        db.session.commit()
        return jsonify({'message': 'Restaurant forbidden successfully'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 400

# Unforbid a restaurant
@restaurant_bp.route('/unforbid/<int:id>', methods=['PATCH'])
@admin_required
def unforbid_restaurant(id):
    try:
        restaurant = Restaurant.query.get_or_404(id)
        restaurant.is_forbidden = False
        db.session.commit()
        return jsonify({'message': 'Restaurant unforbidden successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@restaurant_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        restaurant_data = []
        for restaurant in restaurants:
            # if restaurant.is_forbidden:
            #     continue
            data = restaurant.to_dict()
            is_forbidden = data['is_forbidden']
            data.pop('is_forbidden')
            data['status'] = 'forbided' if is_forbidden else 'normal'
            if restaurant.image:
                data['image'] = f"{request.host_url}{restaurant.image}"
            else:
                data['image'] = f"{request.host_url}static/default/restaurant_default.png"
            if restaurant.qr_code:
                data['qr_code'] = f"{request.host_url}{restaurant.qr_code}"
            else:
                data['qr_code'] = f"{request.host_url}static/default/qr_code_default.png"
            restaurant_data.append(data)
        return jsonify(restaurant_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    
"""---------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------------用户路由-------------------------------------------------"""
"""---------------------------------------------------------------------------------------------------------"""
# Get all restaurants
@restaurant_bp.route('/user_get_all', methods=['GET'])
@jwt_required()
def get_unforbidden_restaurants():
    try:
        restaurants = Restaurant.query.all()
        restaurant_data = []
        for restaurant in restaurants:
            # if restaurant.is_forbidden:
            #     continue
            data = restaurant.to_dict()
            is_forbidden = data['is_forbidden']
            data.pop('is_forbidden')
            data['status'] = 'forbided' if is_forbidden else 'normal'
            if restaurant.image:
                data['image'] = f"{request.host_url}{restaurant.image}"
            else:
                data['image'] = f"{request.host_url}static/default/restaurant_default.png"
            if restaurant.qr_code:
                data['qr_code'] = f"{request.host_url}{restaurant.qr_code}"
            else:
                data['qr_code'] = f"{request.host_url}static/default/qr_code_default.png"
            restaurant_data.append(data)
        return jsonify(restaurant_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Get a restaurant by name
@restaurant_bp.route('/get_by_name', methods=['GET'])
@jwt_required()
def get_restaurant_by_name():
    name = request.args.get('restaurantName')
    print(request.args)
    try:
        restaurant = Restaurant.query.filter_by(name=name).all()
        if restaurant:
            restaurant_data = []
            for r in restaurant:
                data = r.to_dict()
                if r.image:
                    data['image'] = f"{request.host_url}{r.image}"
                if r.qr_code:
                    data['qr_code'] = f"{request.host_url}{r.qr_code}"
                restaurant_data.append(data)
            return jsonify(restaurant_data), 200
        return jsonify({'error': 'Restaurant not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Get a restaurant by id
@restaurant_bp.route('/get_by_id/<int:id>', methods=['GET'])
@jwt_required()
def get_restaurant_by_id(id):
    try:
        restaurant = Restaurant.query.get_or_404(id)
        data = restaurant.to_dict()
        if restaurant.image:
            data['image'] = f"{request.host_url}{restaurant.image}"
        if restaurant.qr_code:
            data['qr_code'] = f"{request.host_url}{restaurant.qr_code}"
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Get restaurant markers (for map display)
@restaurant_bp.route('/marker', methods=['GET'])
@jwt_required()
def get_markers():
    try:
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

