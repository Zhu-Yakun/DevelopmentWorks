# Order backend implementation for Restaurant System
from flask import Blueprint, request, jsonify
from models import Order, db, Restaurant, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy.orm import joinedload
from routes.order_notification import create_order_notification
import json

order_bp = Blueprint('order', __name__)

# status: Created, Shipped, Completed, Deleted

# Create a new order
@order_bp.route('/add', methods=['POST'])
@jwt_required()
def add_order():
    data = request.get_json()
    user_data = get_jwt_identity()
    user_data = json.loads(user_data)
    data['user_id'] = user_data.get('id')
    try:
    # Ensure restaurant, user, and delivery person exist
        restaurant = Restaurant.query.get(data.get('restaurant_id'))

        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        if not data.get('delivery_fee'):
            return jsonify({'error': 'Delivery fee is required'}), 400
        if not data.get('address'):
            return jsonify({'error': 'Address is required'}), 400        
        
        # 将 pickupTime 和 deliveryTime 转换为 datetime 对象
        expected_pickup_time_1 = datetime.fromisoformat(data.get('expected_pickup_time').replace('Z', '+00:00')).astimezone()
        desired_delivery_time_1 = datetime.fromisoformat(data.get('desired_delivery_time').replace('Z', '+00:00')).astimezone()
        
        new_order = Order(
            restaurant_id=data.get('restaurant_id'),
            user_id=data.get('user_id'),
            phone=data.get('phone'),
            gender=data.get('gender'),
            delivery_person_id=None,
            order_date=datetime.now(),
            expected_pickup_time=expected_pickup_time_1,
            desired_delivery_time=desired_delivery_time_1,
            status='Created',
            delivery_fee=data.get('delivery_fee'),
            completion_date=None,
            remarks=data.get('remarks'),
            address=data.get('address'),
            comment_id = None
        )
        db.session.add(new_order)
        db.session.commit()
        create_order_notification('新订单', '您创建了一个新订单', new_order.user_id, new_order.id, 'Order Created')
        return jsonify({'message': 'Order added successfully', 'order': new_order.to_dict()}), 201
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 400

# Get all orders
@order_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# # Update an order
# @order_bp.route('/update/<int:order_id>', methods=['PUT'])
# @jwt_required()
# def update_order(order_id):
#     data = request.get_json()
#     try:
#         order = Order.query.get_or_404(order_id)
#         for key, value in data.items():
#             if hasattr(order, key):
#                 setattr(order, key, value)
#         db.session.commit()
#         return jsonify({'message': 'Order updated successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# Delete an order
@order_bp.route('/delete/<int:order_id>', methods=['PUT'])
@jwt_required()
def delete_order(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        order.status = 'Deleted'
        db.session.commit()
        create_order_notification('订单已删除', '您的订单已删除', order.user_id, order.id, 'Order Deleted')
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 400

# Get orders by order ID
@order_bp.route('/get_order_by_id/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_by_id(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        user = User.query.get(order.user_id)
        restaurant = Restaurant.query.get(order.restaurant_id)
        if order.delivery_person_id is not None:
            delivery_person = User.query.get(order.delivery_person_id)
        order_dict = order.to_dict()
        order_dict['user'] = user.to_dict()
        order_dict['restaurant'] = restaurant.to_dict()
        if order.delivery_person_id is not None:
            order_dict['delivery_person'] = delivery_person.to_dict()
        return jsonify(order_dict), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}") 
        return jsonify({'error': str(e)}), 400

# Get orders by user   
@order_bp.route('/get_by_user', methods=['GET'])
@jwt_required()
def get_orders_by_user():
    user_data = get_jwt_identity()
    user_data = json.loads(user_data)
    try:
        orders = Order.query.filter_by(user_id=user_data['id']).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Get orders by delivery person ID
@order_bp.route('/get_by_delivery_person', methods=['GET'])
@jwt_required()
def get_orders_by_delivery_person():
    user_data = get_jwt_identity()
    user_data = json.loads(user_data)
    try:
        orders = Order.query.filter_by(delivery_person_id=user_data['id']).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Get all Created orders
@order_bp.route('/get_initiated_orders', methods=['GET'])
@jwt_required()
def get_initiated_orders():
    try:
        orders = Order.query.filter_by(status='Created').all()
                 
        orders_all = []
        for order in orders:
            user = User.query.get(order.user_id)
            restaurant = Restaurant.query.get(order.restaurant_id)
            order_dict = order.to_dict()
            order_dict['user'] = user.to_dict() if user else None
            order_dict['restaurant'] = restaurant.to_dict() if restaurant else None
            orders_all.append(order_dict)
            
        return jsonify(orders_all), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# Update order status, get delivery person accepts order
@order_bp.route('/accept_order', methods=['PUT'])
@jwt_required()
def accept_order():
    data = request.get_json()
    try:
        order = Order.query.get(data.get('order_id'))
        delivery_person = User.query.get(data.get('delivery_person_id'))
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        if not delivery_person:
            return jsonify({'error': 'Delivery person ID is required'}), 400
        if order.status != 'Created':
            return jsonify({'error': 'Order has already been accepted'}), 400
        order.status = 'Shipped'
        order.delivery_person_id = delivery_person.id
        db.session.commit()
        create_order_notification('订单已接单', '您的订单已在配送中', order.user_id, order.id, 'Order Shipped')
        create_order_notification('订单已接单', '您接受了一个新订单', delivery_person.id, order.id, 'Order Accepted')
        return jsonify({'message': 'Order accepted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# Update order status, get delivery person rejects order
@order_bp.route('/cancel_order/<int:order_id>', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        if order.status != 'Shipped':
            return jsonify({'error': 'Order has already been accepted'}), 400
        order.status = 'Created'
        order.delivery_person_id = None
        db.session.commit()
        create_order_notification('订单已取消', '您的订单已取消', order.user_id, order.id, 'Order Cancelled')
        return jsonify({'message': 'Order rejected successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Complete order
@order_bp.route('/complete_order', methods=['PUT'])
@jwt_required()
def complete_order():
    data = request.get_json()
    try:
        order = Order.query.get(data.get('order_id'))
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        order.status = 'Completed'
        order.completion_date = datetime.now()
        db.session.commit()
        create_order_notification('订单已完成', '您的订单已完成', order.user_id, order.id, 'Order Completed')
        return jsonify({'message': 'Order completed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# # Update order status, get delivery person rejects order
# @order_bp.route('/reject_order/<int:order_id>', methods=['GET'])
# @jwt_required()
# def reject_order(order_id):
#     try:
#         order = Order.query.get(order_id)
#         if not order:
#             return jsonify({'error': 'Order not found'}), 404
#         if order.status != 'Created':
#             return jsonify({'error': 'Order has already been accepted'}), 400
#         order.status = 'Created'
#         order.delivery_person_id = None
#         db.session.commit()
#         return jsonify({'message': 'Order rejected successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400
