from flask import Blueprint
from flask_login import LoginManager
from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from config import Config

main_opt = Blueprint('main_opt', __name__, static_folder="../static", template_folder="../templates")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)
# session配置
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SECRET_KEY'] = os.urandom(24)
Session(app)
# 数据库配置
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/bigdata?charset=utf8'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# 绑定app和数据库，以便进行操作
migrate = Migrate(app, db)

# 登录配置
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from login.models import User


# 不放这里导致出现No user_loader has been installed for this LoginManager
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# 注册蓝本
from login import login_opt
from about import about_opt

app.register_blueprint(login_opt)
app.register_blueprint(about_opt)
app.register_blueprint(main_opt)

import main.routes
