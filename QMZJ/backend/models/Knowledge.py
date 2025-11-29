from models.modelConfig import db
import datetime
from flask import request

# 数据模型：表示古代知识与现代理论的对应关系
class KnowledgePair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 古代信息部分
    ancient_title = db.Column(db.String(100), nullable=False)
    ancient_description = db.Column(db.String(500), nullable=False)
    ancient_year = db.Column(db.Integer, nullable=False)  # 古代年份
    ancient_img = db.Column(db.String(500), nullable=True, default = None)

    # 现代理论部分
    modern_title = db.Column(db.String(100), nullable=False)
    modern_description = db.Column(db.String(500), nullable=False)
    modern_year = db.Column(db.Integer, nullable=False)  # 现代年份
    modern_img = db.Column(db.String(500), nullable=True, default = None)

    # 添加一对多关系
    list_items = db.relationship('ListItem', backref='knowledge_pair', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'ancient_title': self.ancient_title,
            'ancient_description': self.ancient_description,
            'ancient_year': self.ancient_year,
            'ancient_img': self.ancient_img,
            'modern_title': self.modern_title,
            'modern_description': self.modern_description,
            'modern_year': self.modern_year,
            'modern_img': self.modern_img,
            # 包含关联的列表项
            'list_items': [item.to_dict() for item in self.list_items],
        }

class ListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(500), nullable=True)
    
    # 添加外键关联到KnowledgePair
    pair_id = db.Column(db.Integer, db.ForeignKey('knowledge_pair.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'year': self.year,
            'img': self.img
        }
