from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 64)])
    submit=SubmitField('提交')