from models.modelConfig import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    feedback_type = db.Column(db.String(64))
    feedback_content = db.Column(db.String(256))
    contact = db.Column(db.String(64))