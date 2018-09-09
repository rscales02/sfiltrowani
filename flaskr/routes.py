from flaskr import app
from flask import render_template, flash, redirect, url_for
from flaskr.forms import LoginForm


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # display message to user for successful submit
        flash("Login requested for user {}, remember_me={}".format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)
