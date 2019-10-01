from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Optional


class PostForm(FlaskForm):
    title = StringField(label='Title', default='New post', description='Title of the post', validators=[DataRequired()])
    titleUri = StringField(label='Title URI', default='new-post', description='Custom title URI', validators=[Optional()])
    date = DateTimeField(label='Date', description='d.m.Y', format='%d.%m.%Y', validators=[DataRequired()])
    content = TextAreaField(label='Content', description='Content of the post', default='Lorem Ipsum', validators=[DataRequired()])
    author = StringField(label='Author', description='Author of the post', default='Your Name', validators=[DataRequired()])
    submit = SubmitField('Save')
