from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from hashlib import md5

from main import db

"""
用户表相关model
"""


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # back是反向引用,User和Post是一对多的关系，backref是表示在Post中新建一个
    # 属性author，关联的是Post中的user_id外键关联的User对象。lazy属性常用的值
    # 的含义，select就是访问到属性的时候，就会全部加载该属性的数据;joined则是
    # 在对关联的两个表进行join操作，从而获取到所有相关的对象;
    # dynamic则不一样，在访问属性的时候，并没有在内存中加载数据，而是返回一个
    # query对象, 需要执行相应方法才可以获取对象，比如.all()
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 获取头像
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<用户名:{}>'.format(self.username)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.INTEGER, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post{}>'.format(self.body)
