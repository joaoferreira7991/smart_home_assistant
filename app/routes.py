from app import app, db
from app.models import User, Actuator
from app.forms import UserSignUpForm, UserSignInForm, ActuatorCreateForm
from flask import redirect, url_for, request, render_template, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():  
    form = ActuatorCreateForm()
    if form.validate_on_submit():
        actuator = Actuator(name=form.name.data, ip=form.ip.data)
        db.session.add(actuator)
        db.session.commit()
        flash('{} was added with success!'.format(actuator.name))    
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('index.html', title='Index', user=user, form=form)

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