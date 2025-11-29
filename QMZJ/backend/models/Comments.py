from models.modelConfig import db

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, comment="评论内容")
    create_time = db.Column(db.DateTime, default=db.func.now(), comment="创建时间")
    likes = db.Column(db.Integer, default=0, comment="点赞数")
    
    # 关联用户ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment="用户ID")
    user = db.relationship('User', backref='comments')
    
    # 多态关联字段
    item_name = db.Column(db.String(50), nullable=False, comment="被评论对象的名称")
    item_type = db.Column(db.String(50), nullable=False, comment="被评论对象的类型，例如'NongJu', 'NongShu', 'NongZuoWu', 'NongYeJiShu', 'NongYeWenHua'")
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'create_time': self.create_time,
            'likes': self.likes,
            'user_id': self.user_id,
            'item_name': self.item_name,
            'item_type': self.item_type
        }
