import os
import secrets
from PIL import Image
from flask import Flask, render_template, flash, redirect, url_for, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PitchForm
from app.models import User, Pitch
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def index():
      pitches = Pitch.query.all()
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

# Function to save picture
def save_picture(form_picture):
      random_hex = secrets.token_hex(8)
      _, f_ext = os.path.splitext(form_picture.filename)
      picture_fn = random_hex + f_ext
      picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
      
      form_picture.save(picture_path)
      return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
      form  = UpdateAccountForm()
      if form.validate_on_submit():
            if form.picture.data:
                  picture_file = save_picture(form.picture.data)
                  current_user.image_file = picture_file 

            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated', category='success')
            return redirect(url_for('account'))
      elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
      image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
      return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/logout')
def logout():
      logout_user()
      return redirect(url_for('index'))


@app.route('/add-pitch', methods=['GET', 'POST'])
@login_required
def addPitch():
      form = PitchForm()
      if form.validate_on_submit():
            pitch = Pitch(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(pitch)
            db.session.commit()
            flash('Your Pitch has been added', 'success')
            return redirect(url_for('index'))
      return render_template('add-pitch.html', title='Add PITCH', form=form, legend='New Pitch')


@app.route('/pitch/<int:pitch_id>')
def pitch(pitch_id):
      pitch = Pitch.query.get_or_404(pitch_id)
      return render_template('pitch.html', title=pitch.title, pitch=pitch)


@app.route('/pitch/<int:pitch_id>/update', methods=['GET', 'POST'])
@login_required
def update_pitch(pitch_id):
      pitch = Pitch.query.get_or_404(pitch_id)
      if pitch.author != current_user:
            abort(403)
      form = PitchForm()
      if form.validate_on_submit():
            pitch.title = form.title.data
            pitch.content = form.content.data
            db.session.commit()
            flash('Pitch has been updated', 'success')
            return redirect(url_for('pitch', pitch_id=pitch.id))
      elif request.method == 'GET':
            form.title.data = pitch.title
            form.content.data = pitch.content

      return render_template('add-pitch.html', title='Update PITCH', form=form, legend='Update Pitch')
