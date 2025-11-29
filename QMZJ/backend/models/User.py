from models.modelConfig import db
from werkzeug.security import generate_password_hash



class User(db.Model):
    # 设置表名
    __tablename__ = 'user'
    # id，主键并自动递增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    account = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(256), nullable=True)

    # 设置只可写入，对密码进行加密
    def password_hash(self, password):
        self.password = generate_password_hash(password)

