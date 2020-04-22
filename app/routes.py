from app import app, db
from app.models import User
from app.forms import UserSignUpForm, UserSignInForm
from flask import redirect, url_for, request, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Index')

@app.route('/add-student', methods = ['GET' , 'POST'])
def add_student():
    form = StudentForm()
    if request.method == 'POST':
        student = Students(name=form.name.data, age=form.age.data,
                    address=form.address.data, cellphone=form.cellphone.data,
                    email=form.email.data)
        db.session.add(student)
        db.session.commit()
        flash('Student added with success!')
    return render_template('add-student.html', title='Add Student', form = form)

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