from models.Knowledge import KnowledgePair
from models.User import User
from models.modelConfig import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import Blueprint, request, session, jsonify
from decorators import login_limit
import time

timeline = Blueprint("timeline", __name__, url_prefix="/api/timeline")

@timeline.route('/get_all', methods=['GET'])
@login_limit
def get_timeline():
    print("get_timeline")
    records = KnowledgePair.query.all()
    records_data = []
    for record in records:
        data = record.to_dict()
        if record.ancient_img:
            data['ancient_img'] = f"{request.host_url}{record.ancient_img}"
            print(f"ancient_img:{request.host_url}{record.ancient_img}")
        if record.modern_img:
            data['modern_img'] = f"{request.host_url}{record.modern_img}"
            print(f"modern_img:{request.host_url}{record.modern_img}")
        records_data.append(data)
    return jsonify(records_data), 200


@timeline.route('/get_by_id', methods=['GET'])
@login_limit
def get_timeline_by_id():
    record_id = request.args.get('record_id')
    # 使用.first()获取单个记录
    record = KnowledgePair.query.filter_by(id=record_id).first()
    
    if not record:
        return jsonify({"code": 404, "msg": "Record not found"}), 404
    
    # 获取基础数据
    data = record.to_dict()
    
    # 处理古代图片
    if data['ancient_img']:
        data['ancient_img'] = f"{request.host_url}{data['ancient_img']}"
    
    # 处理现代图片
    if data['modern_img']:
        data['modern_img'] = f"{request.host_url}{data['modern_img']}"
    
    # 处理列表项的图片
    for item in data['list_items']:
        if item['img']:
            item['img'] = f"{request.host_url}{item['img']}"
    
    return jsonify({"code": 200, "data": data}), 200