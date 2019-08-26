#!/usr/bin/python3
# encoding: utf-8
from flask import render_template

from main import db
from . import about_opt


# @about_opt.errorhandler(404)
# def internal_error(error):
#     return render_template('404.html'), 404
#
#
# @about_opt.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500


# 如果使用errorhandler 修饰器，那么只有蓝本中的错误才能触发处理程序。
# 即修饰器由蓝本提供。要想注册程序全局的错误处理程序，必须使用app_errorhandler。
@about_opt.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@about_opt.app_errorhandler(500)
def internal_server_error(e):
    # 如果异常是被一个数据库错误触发，数据库的会话会处于一个不正常的状态，因
    # 此我们必须把会话回滚到正常工作状态在渲染 500 错误页模板之前。
    db.session.rollback()
    return render_template('500.html'), 500
