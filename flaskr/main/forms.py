from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length


class NoticeForm(FlaskForm):
    body = TextAreaField('请输入正文', validators=[DataRequired(), Length(20, 200)])
    submit = SubmitField('发布')


class EventForm(FlaskForm):
    name = StringField('请输入事件', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('发布')


class EventDetailForm(FlaskForm):
    body = StringField('请输入事件', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('发布')


class ResourceForm(FlaskForm):
    body = StringField('请输入资源信息', validators=[DataRequired(), Length(1, 128)])
    link = StringField('请输入资源链接', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('发布')
