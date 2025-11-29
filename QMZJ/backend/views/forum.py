from models.Comments import Comments
from models.User import User
from models.modelConfig import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import Blueprint, request, session, jsonify
from decorators import login_limit
import time
from models.DataTable import NongJu,NongShu,NongZuoWu,NongYeJiShu,NongYeWenHua
from datetime import datetime


comments = Blueprint("comments", __name__, url_prefix="/api/forum")


# 写评论
@comments.route('/writeComments', methods=['POST'])
@login_limit
def write_comments():
    try:
        text = request.json['text']
        print("text:",text)
        item_name = request.json['name']
        item_type = request.json['category']
        if not text:
            return jsonify({"message": "缺少必要字段"}), 400  # Bad Request
        
        user_id = get_jwt_identity()
        create_time = time.strftime("%Y-%m-%d %H:%M:%S")

        create_time = datetime.fromisoformat(create_time.replace('Z', '+00:00')).astimezone()


        user = User.query.filter(User.id == user_id).first()
        comment = Comments(text=text, create_time=create_time, likes=0, user_id=user.id, item_name=item_name,item_type=item_type)
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({"message": "评论成功", "id": comment.id}), 201  # Created
    except Exception as e:
        print('评论报错：', e)
        return jsonify({'error': str(e), 'status': 'fail'}), 400


@comments.route('/likeComments', methods=['POST'])
@jwt_required()
def like_comments():
    comment_id = request.json['id']
    if not comment_id:
        return jsonify({"message": "缺少必要字段"}), 400  # Bad Request
    comment=Comments.query.filter(Comments.id == comment_id).first()
    if not comment:
        return jsonify({"message": "评论不存在"}), 404  # Not Found
    comment.likes += 1
    db.session.commit()
    return jsonify({"message": "点赞成功", "likes": comment.likes}), 200  # OK


# 展示全部评论
@comments.route("/commentsAll", methods=['GET'])
@login_limit
def comments_all():
    comments_list = db.session.query(Comments, User) \
                      .join(User, Comments.user_id == User.id) \
                      .order_by(Comments.create_time.desc()) \
                      .all()
    comments = []
    for comment, user in comments_list:
        comments.append({
            "id": comment.id,
            "text": comment.text,
            "create_time": comment.create_time,
            "likes": comment.likes,
            "username": user.username
        })

    return jsonify({"comments": comments}), 200

mapTable = {
        "农具": "NongJu",
        "农书": "NongShu",
        "农作物": "NongZuoWu",      
        "农业技术": "NongYeJiShu",
        "农业文化": "NongYeWenHua",
      }

# 创建模型映射字典
model_map = {
    "NongJu": NongJu,
    "NongShu": NongShu,
    "NongZuoWu": NongZuoWu,
    "NongYeJiShu": NongYeJiShu,
    "NongYeWenHua": NongYeWenHua
}

@comments.route("/commentsByItem", methods=['GET'])
@login_limit
def comments_by_item():
    try:
        name = request.args.get('name')
        category = request.args.get('category')
        if not name or not category:   
            return jsonify({"message": "缺少必要字段"}), 400  # Bad Request
        
        # 获取对应的表名
        table_name = mapTable.get(category)
        if not table_name:
            return jsonify({"message": "无效的分类"}), 401
        print("表名：", table_name)
        
        # 获取对应的模型类
        model_class = model_map.get(table_name)
        if not model_class:
            return jsonify({"message": "分类模型不存在"}), 402
        print("加载模型类：", model_class)
        
        # 查询目标条目
        target_item = model_class.query.filter_by(name=name).first()
        if not target_item:
            return jsonify({"message": "未找到相关条目"}), 404
        
        # 查询关联评论
        comments_list = db.session.query(Comments, User) \
            .join(User, Comments.user_id == User.id) \
            .filter(
                Comments.item_type == category,
                Comments.item_name == target_item.name
            ) \
            .order_by(Comments.create_time.desc()) \
            .all()
        
        # 构造返回数据
        formatted_comments = []
        for comment, user in comments_list:
            # print("类型：", type(comment.create_time))
            # create_time = datetime.fromisoformat(comment.create_time.replace('Z', '+00:00')).astimezone()
            # print("时间：", create_time)
            # create_time_str = create_time.strftime("%Y-%m-%d %H:%M:%S")
            # print("时间字符串：", create_time_str)
            create_time = comment.create_time
            create_time = create_time.astimezone()
            formatted_comments.append({
                "id": comment.id,
                "text": comment.text,
                "create_time": create_time,
                "likes": comment.likes,
                "username": user.username,
                "item_name": comment.item_name,
                "item_type": comment.item_type
            })
        
        return jsonify({"comments": formatted_comments}), 200
    except Exception as e:
        print('获取评论出错：', e)
        return jsonify({'error': str(e), 'status': 'fail'}), 400
