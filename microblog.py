from app import create_app, db, cli
from app.models import User, Post

application = create_app()
cli.register(application)


@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
