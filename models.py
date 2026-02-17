from database import db
from flask_login import UserMixin

class articles (db.Model):
    __tablename__ = "articles_table"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False, unique=True)
    sub_title = db.Column(db.String(256), nullable=False, unique=True)
    content = db.Column(db.String(256), nullable=False, unique=False)
    create_date = db.Column(db.String(256), nullable=False, unique=False)
    modify_date = db.Column(db.String(256), nullable=False, unique=False)
    likes = db.Column(db.Integer, nullable=False, unique=False)
    favorite = db.Column(db.Boolean, nullable=False, unique=False)

    def __repr__(self):
        return f"<{self.id}>"
    
class users (db.Model, UserMixin):
    __tablename__ = "users_table"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, unique=False)
    name = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False, unique=False)

    def __repr__(self):
        return f"<{self.id}>"