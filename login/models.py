from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from hashlib import md5

from main import db, login_manager

"""
用户表相关model

登录验证需要实现验证接口
提供了一个默认实现UserMixin ：
is_authenticated 方法有一个具有迷惑性的名称。一般而言，这个方法应该只返回 True，除非表示用户的对象因为某些原因不允许被认证。
is_active 方法应该返回 True，除非是用户是无效的，比如因为他们的账号是被禁止。
is_anonymous 方法应该返回 True，如果是匿名的用户不允许登录系统。
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


# 不使用默认实现UserMixin，需要实现所有方法
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nickname = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     posts = db.relationship('Post', backref='author', lazy='dynamic')
#
#     @property
#     def is_authenticated(self):
#         return True
#
#     @property
#     def is_active(self):
#         return True
#
#     @property
#     def is_anonymous(self):
#         return False
#
#     # get_id 方法应该返回一个用户唯一的标识符，以 unicode 格式。我们使用
#     # 数据库生成的唯一的 id。需要注意地是在 Python 2 和 3 之间由于 unicode
#     # 处理的方式的不同我们提供了相应的方式。
#     def get_id(self):
#         try:
#             return unicode(self.id)  # python 2
#         except NameError:
#             return str(self.id)  # python 3
#
#     def __repr__(self):
#         return '<User %r>' % (self.nickname)

# 用于从数据库加载用户。这个函数将会被 Flask-Login 使用
@login_manager.user_loader
def load_user(id):
    # 在 Flask-Login 中的用户 id 永远是 unicode 字符串，因此在我们
    # 把 id 发送给 Flask-SQLAlchemy 之前，把 id 转成整型是必须的，否则会报错！
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.INTEGER, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post{}>'.format(self.body)
