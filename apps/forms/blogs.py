from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField,TextAreaField,SelectField
from wtforms.validators import Regexp,Required, Email,Length,DataRequired,EqualTo
from wtforms import ValidationError

class PostBlogForm(FlaskForm):
    title = StringField('Blog Title',validators=[Length(0,256)])
    body = TextAreaField('Blog Content')
    publish = BooleanField('Publish', [DataRequired()])
    tags = StringField('Meta Tags',validators=[Length(0,300)])
    description = StringField('Meta Description',validators=[Length(0,640)])
    submit = SubmitField('Submit')
    
    
class CommentForm(FlaskForm):
    guest = StringField('Guest name',validators=[Length(0,256)])
    body = TextAreaField('Comment')
    submit = SubmitField('Submit')