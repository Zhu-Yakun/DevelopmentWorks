from flask import Blueprint,jsonify,request
from flask_jwt_extended import get_jwt_identity,jwt_required
from werkzeug.security import check_password_hash
from models.User import User
from models.Comments import Comments
from models.modelConfig import db
from models.Feedback import Feedback
from decorators import login_limit
import time

usercenter = Blueprint("usercenter", __name__, url_prefix="/api/usercenter")

# 修改密码
@usercenter.route("/updatePwd", methods=['POST'])
@jwt_required()
def update():
    oldPwd = request.json["oldPassword"]
    newPwd = request.json["newPassword"]
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if check_password_hash(user.password, oldPwd):
        user.password_hash(newPwd)
        db.session.commit() 
        return jsonify({"message": "密码修改成功！"}), 200  # OK
    else:
        return jsonify({"message": "原密码错误！"}), 400  # Bad Request
    
@usercenter.route('/usercomments', methods=['GET'])
@login_limit
def get_user_comments():
    try:
        user_id = get_jwt_identity()
        comments = Comments.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': comment.id, 'content': comment.text, 'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                         'likes': comment.likes } for comment in comments])
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usercenter.route('/feedback', methods=['POST'])
@login_limit
def send_feedback():
    data = request.json
    user_id = get_jwt_identity()
    feedback = Feedback(
        user_id=user_id,
        rating=data['rating'],
        feedback_type=data['feedback_type'],
        feedback_content=data['feedback_content'],
        contact=data['contact']
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify('Feedback sent successfully'), 200