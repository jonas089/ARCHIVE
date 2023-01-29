from datetime import datetime
from artmuc import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

################
# MySQL syntax #
##########################
# I. Python Command Line #
##########################
'''
Create:
1.  from artmuc.models import User, Post
2.  db.create_all() -> create Tables defined in main.py
3.  user_x = (username='USERNAME',
    email='EMAIL',
    profile_picture_path='PATH',
    password='PASSWORD')
    -> id is assigned automatically
    -> products have a relationship | seperate table 'Post'
4.  db.session.add(user_x)
5.  db.session.commit()
'''
class User(db.Model, UserMixin):
    #Everyone
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(384), nullable=False)
    verified = db.Column(db.String(1), nullable=True, default='0')
    #Artist Only
    artist_key = db.Column(db.String(10), nullable=True)
    profile_picture_path = db.Column(db.String(260), nullable=False, default='default.png')
    biography = db.Column(db.String(250), nullable=True)
    products = db.relationship('Post', backref='author', lazy=True)
    stripe_account_id = db.Column(db.String(21), nullable=True, default='0')
    #Customer Only
    country = db.Column(db.String(50), nullable=False, default='')
    region = db.Column(db.String(50), nullable=False, default='')
    address = db.Column(db.String(50), nullable=False, default='')
    zip = db.Column(db.String(50), nullable=False, default='')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_picture_path}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(25), nullable=False)
    product_description = db.Column(db.String(250), nullable=False)
    product_picture_path = db.Column(db.String(260), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_sold = db.Column(db.String(3), nullable=True, default='No')
    #access shipping information through username of customer / located in User model
    customer_email = db.Column(db.String(20), nullable=False, default='')
    customer_country = db.Column(db.String(50), nullable=False, default='')
    customer_region = db.Column(db.String(50), nullable=False, default='')
    customer_address = db.Column(db.String(50), nullable=False, default='')
    customer_zip = db.Column(db.String(50), nullable=False, default='')
    def __repr__(self):
        return f"Product('{self.id}', '{self.product_name}', '{self.product_price}')"
