#!/usr/bin/python3
# encoding: utf-8
from flask import Blueprint

'''
创建 URL用法： 
Flask 会为蓝本中的全部端点加上一个命名空间，这样就可以在不同的蓝本中使用
相同的端点名定义视图函数，而不会产生冲突。（跨蓝本）在单脚本程序中：index() 
视图函数的URL可使用 url_for(‘index’) 

在蓝图中：index() 视图函数的URL 可使用 url_for(‘main.index’) 
另外，如果在一个蓝图的视图函数或者被渲染的模板中需要链接同一个蓝图中的其他
端点，那么使用相对重定向，只使用一个点使用为前缀。简写形式（命名空间是当前请求所在的蓝本）： 
url_for(‘.index’)
'''
about_opt = Blueprint('about_opt', __name__, static_folder="../static",
                      template_folder="../templates")
from about import routes, forms, errors
