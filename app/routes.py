from app import app, db
from app.models import User, Home, Sensor, Reading, data_type_dict
from app.forms import UserSignUpForm, UserSignInForm, HomeCreateForm, SensorCreateForm
from flask import redirect, url_for, request, render_template, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():      
    user = User.query.filter_by(username=current_user.username).first()
    home = Home.query.filter_by(id=user.home_id).first()
    sensors = Sensor.query.filter_by(home_id=user.home_id).all()
    form = HomeCreateForm()
    if form.validate_on_submit():
    home = Home(name=form.name.data)
    db.session.add(home)
    db.session.commit()
    home = Home.query.filter_by(name=form.name.data).first()
    user = User.query.filter_by(username=current_user.username).first()
    user.home_id = home.id
    db.session.commit()
    flash('Home created with success!')
    return redirect(url_for('index'))
    #form_sensor = SensorCreateForm()    
    #if form_sensor.validate_on_submit():
    #    sensor = Sensor(name=form_sensor.name.data)
    #    sensor.home_id = user.home_id
    #    db.session.add(sensor)
    #    db.session.commit()
    #    flash('Sensor created with success!')
    #    return redirect(url_for('index'))


    return render_template('index.html', title='Index', form=form, form_sensor=form_sensor, user=user, home=home, sensors=sensors)

@app.route('/user/<username>')
@login_required
def user(username):
    pass

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserSignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Signed up with success!')
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html', title='Sign up', form=form)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserSignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Invalid username')
            return redirect(url_for('sign_in'))
        if not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('sign_in'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('sign_in.html', title='Sign in', form=form)

@app.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    logout_user()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    req_data = request.get_json()

    # Implement some sort of security to avoid unwanted injections

    temperature = req_data['temperature']
    humidity = req_data['humidity']
    timestamp = req_data['timestamp']
    data_type = req_data['data_type']

    temperature_reading = Reading(timestamp, temperature, data_type_dict[data_type])
    humidity_reading = Reading(timestamp, humidity, data_type_dict[data_type])
    db.session.add(temperature_reading)
    db.session.add(humidity_reading)
    db.session.commit()

    return ""

