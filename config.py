import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # 安全
    SESSION_TYPE = 'filesystem'
    CSRF_ENABLED = True  # CSRF_ENABLED 配置是为了激活 跨站点请求伪造 保护
    SECRET_KEY = os.urandom(24)  # SECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单。
    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/bigdata?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # mail server settings
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    # administrator list
    ADMINS = ['you@example.com']
    # 打开一个伪造的邮箱服务器：
    # python -m smtpd -n -c DebuggingServer localhost:25
