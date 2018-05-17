from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, AnyOf


class NoticeForm(FlaskForm):
    body = TextAreaField('请输入正文', validators=[DataRequired(), Length(20, 200)])
    submit = SubmitField('发布')


class EventForm(FlaskForm):
    name = StringField('请输入事件', validators=[DataRequired(), Length(1, 128)])
    label = SelectField('类别', choices=[('机房建设', '机房建设'), ('客户施工', '客户施工'), ('机房维护', '机房维护')], coerce=str,
                        validators=[DataRequired()])
    submit = SubmitField('发布')


class EventDetailForm(FlaskForm):
    body = StringField('请输入事件', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('发布')


class ResourceForm(FlaskForm):
    body = StringField('请输入资源信息', validators=[DataRequired(), Length(1, 128)])
    link = StringField('请输入资源链接', validators=[DataRequired(), Length(1, 128)])
    resourceClass = SelectField('类别', choices=[('profession', 'profession'), ('tool', 'tool'), ('other', 'other')], coerce=str,
                        validators=[DataRequired()])
    submit = SubmitField('发布')
