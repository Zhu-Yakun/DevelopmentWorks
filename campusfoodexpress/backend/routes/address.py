from models import ShippingAddr, db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

address_bp = Blueprint('address', __name__)

@address_bp.route('/add', methods=['POST'])
@jwt_required()
def create_address():
    """Create a new shipping address."""
    data = request.json
    user_data = get_jwt_identity()
    user_id = json.loads(user_data)['id']
    name = data.get('contactName')
    phone = data.get('phone')
    gender = data.get('contactGender')
    location = data.get('location')
    tag = data.get('tag')
    lat = data.get('lat')
    lng = data.get('lng')

    address = ShippingAddr(
        user_id=user_id,
        name=name,
        phone=phone,
        gender=gender,
        location=location,
        tag=tag,
        lat=lat,
        lng=lng
    )
    db.session.add(address)
    db.session.commit()

    return jsonify({"message": "Address created successfully", "address": address.to_dict()}), 201

@address_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_addresses():
    """Get all shipping addresses."""
    user_data = get_jwt_identity()
    user_id = json.loads(user_data)['id']
    addresses = ShippingAddr.query.filter_by(user_id=user_id).all()
    result = [address.to_dict() for address in addresses]
    return jsonify({"addresses": result}), 200

@address_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    """Delete a shipping address."""
    user_data = get_jwt_identity()
    user_id = json.loads(user_data)['id']
    address = ShippingAddr.query.filter_by(id=id, user_id=user_id).first()
    if not address:
        return jsonify({"message": "Address not found"}), 404
    db.session.delete(address)
    db.session.commit()
    return jsonify({"message": "Address deleted successfully"}), 200