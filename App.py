from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] ='dbb0a75595cd8924bd0ec31c43898697'

posts = [
      {
            'author': 'Nimrod Allan',
            'title': 'Business Pitch',
            'content': 'Winning a Business Pitch',
            'date_posted': 'May 11, 2022'
      },
      {
            'author': 'John Doe',
            'title': 'Creative Pitch',
            'content': 'lorem Ipsum dlorum sit amet, consectetur',
            'date_posted': 'May 10, 2022'
      }
]

@app.route('/')
@app.route('/home')
def index():
      return render_template('index.html', posts=posts)


@app.route('/about')
def about():
      return render_template('about.html')


@app.route('/register')
def register():
      form = RegistrationForm()
      return render_template('register.html', title='Regsiter', form=form)


@app.route('/login')
def login():
      form = LoginForm()
      return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
      app.run(debug=True)