from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    location = StringField('Location', validators=[DataRequired(), Length(max=50)])
    bio = TextAreaField('Bio', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Save Changes')