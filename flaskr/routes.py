from datetime import datetime
from flaskr import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from flaskr.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, \
    ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from flaskr.email import send_password_reset_email
from flaskr.models import User, Post
from werkzeug.urls import url_parse
from flask_babel import _
from guess_language import guess_language
from flaskr import translate

@app.before_request
def before_request():
    """
    once user logs in, update 'last seen' to current time and commit to database
    :return: nothing
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    create main home index page w/ ability to write and post to blog
    :return: a render of the home index page
    """
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language is 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home page', form=form, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    create log-in page with log-in form
    :return: a render of the log-in page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid Username or Password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    """
    log user out
    :return: redirect to home index page
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    register a new user with username and password
    :return: renders the registration page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    """
    create User profile
    :param username: valid username string
    :return: render User Profile page
    """
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    create form/page to edit User profile
    :return: renders edit User Profile page
    """
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    """
    allow Users to follow other users
    :param username: valid username string
    :return: renders user profile page
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_("You can't follow yourself... narcissist"))
        return redirect(url_for('index'))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s', username=username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    """
    allow Users to unfollow other users
    :param username: valid username string
    :return: redirect to user profile
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_("You can't unfollow yourself"))
        return redirect(url_for('index'))
    current_user.unfollow(user)
    db.session.commit()
    flash(_("You aren't following %(username)s", username=username))
    return redirect('user', username=username)


@app.route('/explore')
@login_required
def explore():
    """
    allow Users to discover other users and see recent activity
    :return: renders Explore page, a list of User posts in timestamp order
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    renders password reset request form
    :return: renders password reset request form page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for instructions on how to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title="Reset Password", form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    allow users to reset their password
    :param token: valid, unexpired token generated by user trying to reset password
    :return: renders password reset form
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/translate', methods=["POST"])
@login_required
def translate_text():
    """
    send json to be translated
    :return: packaged json to be sent to back to client
    """
    return jsonify({
        'text': translate(request.form['text'], request.form['source_language'], request.form['dest_language'])
    })


