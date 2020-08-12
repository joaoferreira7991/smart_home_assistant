from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField, DateTimeField, FloatField, TimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

data_required = 'Required Field.'

class UserSignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(data_required)])
    password = PasswordField('Password', validators=[DataRequired(data_required)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UserSignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(data_required)])
    email = StringField('Email', validators=[DataRequired(data_required), Email()])
    password = PasswordField('Password', validators=[DataRequired(data_required)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(data_required), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already in use.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already in use.')

class ScheduleForm(FlaskForm):
    timestamp = TimeField('timestamp', validators=[DataRequired(data_required)])
    actuator_id = IntegerField('actuator_id', validators=[DataRequired(data_required)])
    submit = SubmitField('Schedule')

'''
class SensorCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(data_required)])
    submit = SubmitField('Create')

class ActuatorCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(data_required)])
    submit = SubmitField('Create')

class ReadingCreateForm(FlaskForm):
    timestamp = DateTimeField('timestamp', validators=[DataRequired()])
    data_reading = FloatField('data_reading', validators=[DataRequired()])
    submit = SubmitField('submit')
'''