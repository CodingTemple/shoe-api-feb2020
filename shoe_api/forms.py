from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Email, EqualTo, DataRequired


# UserSignUp Form
class UserForm(FlaskForm):
    email = StringField('Email', validators=[Email(),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField()
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()