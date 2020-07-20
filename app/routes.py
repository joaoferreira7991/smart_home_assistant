from app import app, db
from app.models import User, Home, Sensor, Reading, data_type_dict
from app.forms import UserSignUpForm, UserSignInForm, HomeCreateForm, SensorCreateForm
from flask import redirect, url_for, request, render_template, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

import app.socketio_server

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():      
    user = User.query.filter_by(username=current_user.username).first()
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
    
    # Checks if home is already assigned, if it is then loads a list of the readings, separated from
    # reading type.
    if user.home_id is not None:
        socketio.start_background_task(example)
        home_name = Home.query.get(user.home_id)
        temperature_list = Reading.query.filter_by(data_type=data_type_dict['dht11_temperature']).all()
        humidity_list = Reading.query.filter_by(data_type=data_type_dict['dht11_humidity']).all()
        return render_template('index.html', title='Index', form=form, user=user, home_name=home_name, temperature_list=temperature_list, humidity_list=humidity_list)
    else:
        return render_template('index.html', title='Index', form=form, user=user)

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


