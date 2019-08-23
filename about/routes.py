#!/usr/bin/python3
# encoding: utf-8
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from about import about_opt
from about.forms import EditProfileForm
from login.models import User
from main import db


@about_opt.route('/user/<username>')
@login_required  # 需要登录验证
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': '测试Post #1号'},
        {'author': user, 'body': '测试Post #2号'}
    ]

    return render_template('user.html', user=user, posts=posts)


@about_opt.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('你的提交已变更.')
        return redirect(url_for('about_opt.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑', form=form)
