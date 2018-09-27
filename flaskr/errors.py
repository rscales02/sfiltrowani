from flask import render_template
from flaskr import app, db


@app.errorhandler(404)
def not_found_error(error):
    """
    handle 404 page not found error
    :param error: 404 page not found error
    :return: renders 404, page not found page
    """
    print(error)
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    handle internal error 500
    :param error: internal error 500
    :return: render internal error 500 page
    """
    db.session.rollback()
    return render_template('500.html'), 500
