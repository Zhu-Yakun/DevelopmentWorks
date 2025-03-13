"""The models for database."""
from extensions import db
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import json

# # Test Data Lists
# test_data_list_users = [
#     {
#         'nickname': 'JohnDoe',
#         'phone': '123456',
#         'password': '1',
#         'bio': 'Food enthusiast',
#         'avatar': 'static/uploads/avatars/avatar1.png',
#         'is_admin': False,
#         'is_forbidden': False,
#         'auth_status': ''
#     },
#     {
#         'nickname': 'JaneSmith',
#         'phone': '456789',
#         'password': '1',
#         'bio': 'Loves Italian food',
#         'avatar': 'static/uploads/avatars/avatar2.png',
#         'is_admin': False,
#         'is_forbidden': False,
#         'auth_status': ''
#     },
#     {
#         'nickname': 'AdminUser',
#         'phone': '111',
#         'password': '1',
#         'bio': 'Restaurant Manager',
#         'avatar': 'static/uploads/avatars/avatar3.png',
#         'is_admin': False,
#         'is_forbidden': False,
#         'auth_status': ''
#     }
# ]

test_data_list_restaurants = [
    {
        "name": "test1",
        "address": "123 Test St, Test City",
        "lat": 40.7128,
        "lng": -74.0060,
        "phone": "123-456-7890",
        "qr_code": "static/uploads/restaurants/1/QR.png",
        "description": "This is test restaurant 1.",
        "sales": 100,
        "image": "static/uploads/restaurants/1/BA.png",
        "is_forbidden": False,
        'rating': 4.8
    },
    {
        "name": "test2",
        "address": "456 Example Ave, Sample Town",
        "lat": 34.0522,
        "lng": -118.2437,
        "phone": "987-654-3210",
        "qr_code": "static/uploads/restaurants/2/QR.png",
        "description": "This is test restaurant 2.",
        "sales": 200,
        "image": "static/uploads/restaurants/2/BA.png",
        "is_forbidden": False,
        'rating': 4.8
    }
]

# test_data_list_orders = [
#     {
#         'restaurant_id': 1,
#         'user_id': 1,
#         'phone': '1234567890',
#         'gender': "女士",
#         'delivery_person_id': '',
#         'order_date': datetime.now(),
#         'status': '空闲中',
#         'delivery_fee': 5.0,
#         'completion_date': None,
#         'remarks': 'Please deliver between 3-5 PM',
#         'address': '123 Main Street, City, State',
#     },
#     {
#         'restaurant_id': 2,
#         'user_id': 2,
#         'phone': '1234567890',
#         'gender': "先生",
#         'delivery_person_id': 1,
#         'order_date': datetime.now(),
#         'status': '进行中',
#         'delivery_fee': 7.5,
#         'completion_date': None,
#         'remarks': 'Call me when you arrive',
#         'address': '456 Park Avenue, City, State'
#     }
# ]

# User Model
class User(db.Model):
    """User model wrapper."""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(256))
    avatar = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    is_forbidden = db.Column(db.Boolean, default=False)
    auth_status = db.Column(db.String(20), default='unauthorized', nullable=False)
    
    def set_password(self, password: str):
        """Set the password.

        Args:
            password (str): The string for the password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        """The validation for the password.

        Args:
            password (str): The string for the password.
        """
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """Generate JWT for user authentication
        
        Returns:
            token (str): The JWT string.
        """
        identity_data = json.dumps({'id': self.id, 'is_admin': self.is_admin})
        return create_access_token(identity=identity_data)
    
    # def init():
    #     for test_data in test_data_list_users:
    #         if not User.query.filter_by(phone=test_data['phone']).first():
    #             new_user = User(
    #                 nickname=test_data['nickname'],
    #                 phone=test_data['phone'],
    #                 password_hash=generate_password_hash(test_data['password']),
    #                 bio=test_data['bio'],
    #                 avatar=test_data['avatar'],
    #                 is_admin=test_data['is_admin'],
    #                 is_forbidden=test_data['is_forbidden'],
    #                 auth_status=test_data['auth_status']
    #             )
    #             db.session.add(new_user)
    #     db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'phone': self.phone,
            'bio': self.bio,
            'avatar': self.avatar,
            'is_admin': self.is_admin,
            'is_forbidden': self.is_forbidden,
            'auth_status': self.auth_status
        }

# Restaurant Model
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    qr_code = db.Column(db.String(255), nullable=True)
    is_forbidden = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(255), nullable=True)
    sales = db.Column(db.Integer, default=0)
    image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    rating = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'lat': self.lat,
            'lng': self.lng,
            'phone': self.phone,
            'qr_code': self.qr_code,
            'is_forbidden': self.is_forbidden,
            'description': self.description,
            'sales': self.sales,
            'image': self.image,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'rating': self.rating
        }

    # @staticmethod
    # def init():
    #     for test_data in test_data_list_restaurants:
    #         new_restaurant = Restaurant(
    #             name=test_data['name'],
    #             address=test_data['address'],
    #             phone=test_data['phone'],
    #             qr_code=test_data['qr_code'],
    #             is_forbidden=test_data['is_forbidden'],
    #             description=test_data['description'],
    #             sales=test_data['sales'],
    #             image=test_data['image'],
    #             lat=test_data['lat'],
    #             lng=test_data['lng'],
    #             rating=test_data['rating']
    #         )
    #         db.session.add(new_restaurant)
    #     db.session.commit()

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    delivery_person_id = db.Column(db.Integer, nullable=True)
    order_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    expected_pickup_time = db.Column(db.DateTime, nullable=True)
    desired_delivery_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='空闲中')
    delivery_fee = db.Column(db.Float, nullable=False, default=0.0)
    completion_date = db.Column(db.DateTime, nullable=True)
    remarks = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='SET NULL'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'user_id': self.user_id,
            'phone': self.phone,
            'gender': self.gender,
            'delivery_person_id': self.delivery_person_id,
            'order_date': self.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'expected_pickup_time': str(self.expected_pickup_time) if self.expected_pickup_time else None,
            'desired_delivery_time': str(self.desired_delivery_time) if self.desired_delivery_time else None,
            'status': self.status,
            'delivery_fee': self.delivery_fee,
            'completion_date': str(self.completion_date) if self.completion_date else None,
            'remarks': self.remarks,
            'address': self.address,
            'is_commented': True if self.comment_id else False
        }

# status: Created, Shipped, Completed, Deleted
        
class VerificationRequest(db.Model):
    """实名认证请求表."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    real_name = db.Column(db.String(80), nullable=False)
    id_number = db.Column(db.String(20), nullable=False)
    document_image = db.Column(db.String(255), nullable=True)  # 新增字段
    status = db.Column(db.String(20), default='unauthorized', nullable=False)# 状态
    request_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    review_date = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)

    def to_dict(self):
        """将认证请求信息转换为字典格式."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'real_name': self.real_name,
            'id_number': self.id_number,
            'document_image': self.document_image,
            'status': self.status,
            'request_date': str(self.request_date),
            'review_date': str(self.review_date) if self.review_date else None,
            'reviewed_by': self.reviewed_by
        }
    @validates('status')
    def validate_status(self, key, value):
        """检查认证状态是否为已审核."""
        if value in ['authorized','unauthorized','pending']:
            return value
        return ValueError("Status must be authorized, unauthorized, or pending")
        
class Favorite(db.Model):
    """用户收藏餐馆模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id',ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # 通过外键建立关系，方便查询
    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    restaurant = db.relationship('Restaurant', backref=db.backref('favorited_by', lazy=True))

    # 设置唯一约束，防止用户重复收藏同一家餐馆
    __table_args__ = (db.UniqueConstraint('user_id', 'restaurant_id', name='unique_user_restaurant'),)

class Status(db.Model):
    """用户状态表."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)
    status_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # 新增字段

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status_id': self.status_id,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }

class Report(db.Model):
    """举报表."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    review_date = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'image_path': self.image_path,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'review_date': str(self.review_date) if self.review_date else None,
            'reviewed_by': self.reviewed_by
        }

class Comment(db.Model):
    """评论表."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    images = db.Column(db.String(511), nullable=True) # 字符串，image地址用分号分隔：image1;image2;image3
    is_anonymous = db.Column(db.Boolean, default=False, nullable=False)  # 是否匿名

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'restaurant_id': self.restaurant_id,
            'order_id': self.order_id,
            'text': self.text,
            'rating': self.rating,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'images': self.images
        }
    
    @validates('rating')
    def validate_rating(self, key, value):
        """Ensure rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value
    @validates('images')
    def validate_imgs_cnts(self, key, value):
        """Ensure the number of images is less than 4."""
        if value and len(value.split(';')) > 3:
            raise ValueError("The number of images should be less than 4")
        return value

class Friendship(db.Model):
    """用户好友关系表."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)  # 当前用户ID
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)  # 好友ID
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # 关系创建时间
    last_read_time = db.Column(db.DateTime, nullable=True)  # user_id最后阅读消息时间
    # 关系字段：便于查询好友用户信息
    user = db.relationship('User', foreign_keys=[user_id], backref='friendships', lazy=True)
    friend = db.relationship('User', foreign_keys=[friend_id], backref='friends_with', lazy=True)

    # 设置唯一约束，防止重复添加好友关系
    __table_args__ = (
        db.UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),
    )

    def to_dict(self):
        """将好友关系转换为字典."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "friend_id": self.friend_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "last_read_time": self.last_read_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_read_time else None
        }

# 干饭小群表
class EatingGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 群聊ID
    name = db.Column(db.String(100), nullable=False)  # 群聊名称
    description = db.Column(db.String(255), nullable=True)  # 群聊描述
    created_at = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    latest_message_id = db.Column(db.Integer, nullable=True)  # 最新消息ID
    owner_user_id = db.Column(db.Integer, nullable=False)  # 群聊所有者ID
    image = db.Column(db.String(255), nullable=True)  # 群聊图片

    # 使用back_populates
    members = db.relationship('EatingGroupMember', back_populates='group', lazy=True)
    # # messages = db.relationship('EatingGroupMessage', backref='eating_group_message', lazy=True)
    # messages = db.relationship('Message', back_populates='group', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'latest_message_id': self.latest_message_id,
            'owner_user_id': self.owner_user_id,
            'members': [member.to_dict() for member in self.members],
            # 'messages': [message.to_dict() for message in self.messages],
            'image': self.image
        }
    def to_dict_without_messages(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'owner_user_id': self.owner_user_id,
            'members': [member.to_dict() for member in self.members],
            'image': self.image,
            # 'latest_message': self.latest_message.to_dict() if self.latest_message else None
        }

    
# 群聊人员表
class EatingGroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 群聊成员ID
    user_id = db.Column(db.Integer, nullable=False)  # 用户ID
    role = db.Column(db.String(50), nullable=False, default='member')  # 成员身份（默认是普通成员）
    group_id = db.Column(db.Integer, db.ForeignKey('eating_group.id', ondelete='CASCADE'), nullable=False)  # 群聊ID
    joined_at = db.Column(db.DateTime, default=datetime.now)  # 加入时间
    last_read_time = db.Column(db.DateTime, nullable=True)  # 最后阅读消息时间
    group = db.relationship('EatingGroup', back_populates='members', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role': self.role,
            'group_id': self.group_id,
            'last_read_time': str(self.last_read_time) if self.last_read_time else None,
            'joined_at': str(self.joined_at)
        }
    
# role：成员身份，有两种取值：member 和 owner

class Message(db.Model):
    """消息表."""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)  # 发送者ID
    content = db.Column(db.Text, nullable=False)  # 消息内容
    content_type = db.Column(db.String(10), nullable=False, default='text')  # 消息类型，默认 'text'
    timestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())  # 消息发送时间
    group_id = db.Column(db.Integer, db.ForeignKey('eating_group.id',ondelete='SET NULL'), nullable=True)  # 群聊ID
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='SET NULL'), nullable=True)  # 接收者ID

    # 关系字段：便于查询相关用户和群聊
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages', lazy=True)
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages', lazy=True)

    def to_dict(self):
        """将消息信息转换为字典."""
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": str(self.content),
            "content_type": self.content_type, 
            "timestamp": str(self.timestamp),
            "group_id": self.group_id,
            "receiver_id": self.receiver_id,
        }

    @validates('content_type')
    def validate_content_type(self, key, value):
        """确保消息类型是预定义的类型."""
        allowed_types = ['text', 'link']
        if value not in allowed_types:
            raise ValueError(f"Content type must be one of {allowed_types}.")
        return value
    
    # @staticmethod
    # def init():
    #     """初始化一些测试消息数据."""
    #     test_messages = [
    #         {"sender_id": 1, "content": "Hello, Bob!", "receiver_id": 2},  # 一对一消息
    #         {"sender_id": 2, "content": "Hi, Alice!", "receiver_id": 1},  # 一对一消息
    #         {"sender_id": 1, "content": "Welcome to the group!", "group_id": 1},  # 群聊消息
    #         {"sender_id": 2, "content": "Thanks, Alice!", "group_id": 1},  # 群聊消息
    #     ]
    #     for message in test_messages:
    #         new_message = Message(
    #             sender_id=message["sender_id"],
    #             content=message["content"],
    #             group_id=message.get("group_id"),
    #             receiver_id=message.get("receiver_id")
    #         )
    #         db.session.add(new_message)
    #     db.session.commit()

class SystemNotification(db.Model):
    """系统消息表."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # 消息标题
    content = db.Column(db.Text, nullable=False)  # 消息内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)  # 接收用户ID
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # 消息创建时间
    is_read = db.Column(db.Boolean, default=False)  # 是否已读
    type = db.Column(db.String(50), nullable=False)  # 消息类型: 用户被禁、实名认证、举报处理、系统广播、其他

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': self.is_read,
            'type': self.type
        }
    
    def to_simple_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': self.is_read
        }

    @validates('title')
    def validate_title_length(self, key, value):
        """确保标题长度不超过200个字符."""
        if len(value) > 200:
            raise ValueError("Title must not exceed 200 characters.")
        return value

    @validates('type')
    def validate_type(self, key, value):
        """确保消息类型是预定义的类型."""
        allowed_types = ['User Ban', 'Real-Name Authentication', 'Report Handling', 'System Broadcast', 'Others']
        if value not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}.")
        return value
# 用户被禁: User Ban
# 实名认证: Real-Name Authentication
# 举报处理: Report Handling
# 系统广播: System Broadcast
# 其他: Others


class OrderNotification(db.Model):
    """订单通知表."""
    id = db.Column(db.Integer, primary_key=True)  # 通知ID
    order_id = db.Column(db.Integer, nullable=False)  # 关联的订单ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)  # 接收通知的用户ID
    title = db.Column(db.String(200), nullable=False)  # 通知标题
    content = db.Column(db.Text, nullable=False)  # 通知内容
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # 创建时间
    is_read = db.Column(db.Boolean, default=False)  # 是否已读
    type = db.Column(db.String(50), nullable=False)  # 通知类型，例如 "Order Created", "Order Shipped", "Order Completed", "Order Cancelled"

    def to_dict(self):
        """将对象转换为字典格式，便于前端使用."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': self.is_read,
            'type': self.type
        }

    def to_simple_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': self.is_read
        }
    
    @validates('title')
    def validate_title_length(self, key, value):
        """确保标题长度不超过200个字符."""
        if len(value) > 200:
            raise ValueError("Title must not exceed 200 characters.")
        return value

    @validates('type')
    def validate_type(self, key, value):
        """确保消息类型是预定义的类型."""
        allowed_types = ['Order Created', 'Order Shipped', 'Order Completed', 'Order Cancelled', 'Order Deleted', 'Order Accepted', 'Order Commented']
        if value not in allowed_types:
            raise ValueError(f"Type must be one of {allowed_types}.")
        return value
    
    # 订单创建：Order Created
    # 订单配送：Order Shipped
    # 订单接收：Order Accepted 配送员接收订单
    # 订单完成：Order Completed
    # 订单取消：Order Cancelle
    # 订单删除: Order Deleted
    # 订单评论：Order Commented

class ShippingAddr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    tag = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    # #经纬度
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'gender':self.gender,
            'phone': self.phone,
            'tag': self.tag,
            'location': self.location,
            'lat': self.lat,
            'lng': self.lng
        }
    
    @validates('gender')
    def validate_gender(self, key, value):
        """Ensure gender is '先生' or '女士'."""
        if value not in ['先生', '女士']:
            raise ValueError('Value must be "先生" or "女士"')
        return value
    
    @validates('tag')
    def validate_tag(self, key, value):
        """Ensure tag is '家' or '公司'."""
        if value not in ['宿舍','实验室','外卖柜','其他']:
            raise ValueError('Value must be "宿舍" or "实验室" or "外卖柜" or "其他"')
        return value