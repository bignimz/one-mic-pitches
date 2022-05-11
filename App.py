from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == '__main__':
      app.run(debug=True)