from flask import Blueprint

login_opt = Blueprint('login_opt', __name__, static_folder="../static", template_folder="../templates")

import login.routes
