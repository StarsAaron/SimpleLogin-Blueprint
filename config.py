import os

class Config(object):
    SESSION_TYPE = 'filesystem'
    CSRF_ENABLED = True  # CSRF_ENABLED 配置是为了激活 跨站点请求伪造 保护
    SECRET_KEY = os.urandom(24)  #SECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单。
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/bigdata?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
