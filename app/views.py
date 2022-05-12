from flask import Flask, render_template, flash, redirect, url_for, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Pitch
from flask_login import login_user, current_user, logout_user, login_required


pitches = [
      {
            'authors': 'Nimrod Allan',
            'title': 'Business Pitch',
            'content': 'Winning a Business Pitch',
            'date_posted': 'May 11, 2022'
      },
       {
            'authors': 'Nimrod Allan',
            'title': 'Business Pitch',
            'content': 'Winning a Business Pitch',
            'date_posted': 'May 11, 2022'
      }
]

@app.route('/')
@app.route('/home')
def index():
      return render_template('index.html', pitches=pitches)


@app.route('/about')
def about():
      return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
      if current_user.is_authenticated:
            return redirect(url_for('index'))
      form = RegistrationForm()
      if form.validate_on_submit():
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
            db.session.add(user)
            db.session.commit()
            flash(f'Account for {form.username.data} was successfully created! You can now login', category='success')
            return redirect(url_for('login'))
      return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
      if current_user.is_authenticated:
            return redirect(url_for('login'))
      form = LoginForm()
      if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                  login_user(user, remember=form.remember.data)
                  next_page = request.args.get('next')
                  return redirect(next_page) if next_page else redirect(url_for('account'))
            else:
                  flash('Login failed! Please check email and password', category='error')

      return render_template('login.html', title='Login', form=form)



@app.route('/account')
@login_required
def account():
      image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
      return render_template('account.html', title='Account', image_file=image_file)


@app.route('/logout')
def logout():
      logout_user()
      return redirect(url_for('index'))


@app.route('/add-pitch')
def addPitch():
      return render_template('add-pitch.html')