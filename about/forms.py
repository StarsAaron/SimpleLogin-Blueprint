from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名!')])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')