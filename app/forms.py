from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    name = StringField('Name')
    location = StringField('Location')
    bio = TextAreaField('Bio')
    email = EmailField('Email', validators=[Email()])
    submit = SubmitField('Save Changes')