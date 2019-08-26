#!/usr/bin/python3
# encoding: utf-8
from flask import flash, redirect, url_for, request, render_template
from flask_login import current_user, login_user, logout_user

from login import login_opt
from login.forms import LoginForm, RegistrationForm
from login.models import User
from main import db


@login_opt.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    '''
    validate_on_submit
    方法做了所有表单处理工作。当表单正在展示给用户的时候调用它，它会返回False.
    如果validate_on_submit在表单提交请求中被调用，它将会收集所有的数据，对字段
    进行验证，如果所有的事情都通过的话，它将会返回True，表示数据都是合法的。
    '''
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效用户名或密码')
            return redirect(url_for('login_opt.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_for(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@login_opt.route('/logout')
def logout():
    logout_user()  # 调用自带utils的退出登录逻辑
    return redirect(url_for('index'))


@login_opt.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户')
        return redirect(url_for('login_opt.login'))
    return render_template('register.html', title='注册', form=form)
