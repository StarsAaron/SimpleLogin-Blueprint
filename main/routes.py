from flask import render_template

from main import app


@app.route('/')
@app.route('/index')
# @login_required
def index():
    user = {'username': 'kevin'}
    posts = [
        {
            'author': {'username': '刘'},
            'body': '这是模板模块中的循环例子～1'
        },
        {
            'author': {'username': '忠强'},
            'body': '这是模板模块中的循环例子～2'
        }
    ]
    return render_template('index.html', title='首页', user=user, posts=posts)