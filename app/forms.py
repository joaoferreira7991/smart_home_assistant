from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField, DateTimeField, FloatField, TimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, ControllerLed, Actuator

data_required = 'Required Field.'

# Handles unique validation errors
class Unique(object):
    def __init__(self, model, field, message='This element already exists.'):
        self.model = model
        self.field = field

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

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

class ActuatorCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(data_required),
        Unique(
            Actuator, 
            Actuator.name,
            message='This name was already used!')])
    ip = StringField('Ip Address', validators=[DataRequired(data_required),
        Unique(
            Actuator, 
            Actuator.ip, 
            message='This ip was already assigned!')])
    submitActuator = SubmitField('Add')

class ControllerCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(data_required),
        Unique(
            ControllerLed, 
            ControllerLed.name, 
            message='This name was already assigned!')])    
    red = IntegerField('Red GPIO Pin', validators=[DataRequired(data_required)])
    green = IntegerField('Green GPIO Pin', validators=[DataRequired(data_required)])
    blue = IntegerField('Blue GPIO Pin', validators=[DataRequired(data_required)])
    submitController = SubmitField('Add')    


'''
class SensorCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(data_required)])
    submit = SubmitField('Create')



class ReadingCreateForm(FlaskForm):
    timestamp = DateTimeField('timestamp', validators=[DataRequired()])
    data_reading = FloatField('data_reading', validators=[DataRequired()])
    submit = SubmitField('submit')
'''