from models.modelConfig import db
import datetime
class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # 关联用户 ID
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 更新时间
    is_pet = db.Column(db.Boolean, default=False)  # 是否为宠物，默认为False

    def __repr__(self):
        return f"<Conversation {self.id}, User {self.user_id}, Created {self.created_at}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_pet": self.is_pet
        }
    
    def __init__(self, id, user_id, is_pet):
        self.id = id
        self.user_id = user_id
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.is_pet = is_pet

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)  # 发送者 ID
    role = db.Column(db.String(50), nullable=False)  # 'user' 或 'assistant'
    content = db.Column(db.Text, nullable=False)  # 消息内容
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)  # 发送时间

    def __repr__(self):
        return f"<Message {self.id}, {self.role}, {self.timestamp}>"

    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }

    def __init__(self, conversation_id, role, content, user_id):
        self.conversation_id = conversation_id
        self.role = role
        self.content = content
        self.user_id = user_id