# define flask app instance
from flaskr import app, db
from flaskr.models import User, Post


@app.shell_context_processor
def make_shell_context():
    # give defaults for flask shell command
    return {'db': db, 'User': User, "Post": Post}