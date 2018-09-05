from flaskr import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Alex'}
    title = 'Sfiltrowani - Czyste Powietrze'
    posts = [
        {
            'author': {'username': 'Alex'},
            'body': "teeth, and healthy breathing"
        },
        {
            'author': {'username': 'Bob'},
            'body': 'drugs and travel'
        }
    ]
    return render_template('index.html', title=title, user=user, posts=posts)
