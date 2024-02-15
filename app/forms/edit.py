from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(max=50)], default="John Doe"
    )
    location = StringField(
        "Location", validators=[DataRequired(), Length(max=50)], default="Dummy City"
    )
    bio = TextAreaField(
        "Bio",
        validators=[DataRequired(), Length(max=500)],
        default="This is a mock bio.",
    )
    submit = SubmitField("Save Changes")
