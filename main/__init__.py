import logging
import os
from datetime import datetime
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Blueprint, g
from flask_login import LoginManager, current_user
from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from config import Config

main_opt = Blueprint('main_opt', __name__, static_folder="../static", template_folder="../templates")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)
# session配置
Session(app)
# 数据库配置
# Flask-SQLAlchemy 管理我们应用程序的数据。这个扩展封装了 SQLAlchemy 项目，这是一个 对象关系映射器 或者 ORM。
db = SQLAlchemy(app)
# 绑定app和数据库，跟踪数据库的更新迁移
migrate = Migrate(app, db)
# 登录配置
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 注册蓝本
from login import login_opt
from about import about_opt

app.register_blueprint(login_opt)
app.register_blueprint(about_opt)
app.register_blueprint(main_opt)


# 注册登录的用户到全局变量 flask.g 中
@app.before_request
def before_request():
    # 全局变量 current_user 是被 Flask-Login 设置的，因此我
    # 们只需要把它赋给 g.user ，让访问起来更方便。
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


if not app.debug:
    # 方式一：邮件发送错误信息
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # 方式二：错误信息记录到文件
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from main import routes
