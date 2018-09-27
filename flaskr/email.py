from flask_mail import Message
from flaskr import mail, app
from flask import render_template
from threading import Thread
from flask_babel import lazy_gettext as _l


def send_email(subject, sender, recipients, text_body, html_body):
    """
    send email
    :param subject: expects subject string
    :param sender: expects valid sender email string
    :param recipients: expects valid list of email strings
    :param text_body: expects message string
    :param html_body: expects HTML markup for email
    :return: nothing
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    """
    send password reset email
    :param user: expects valid username string
    :return: nothing
    """
    token = user.get_reset_password_token()
    send_email(
        _l('Sfiltrowani Password Reset'),
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token)
    )


def send_async_email(app, message):
    """
    asynchronously send mail and prevent app freeze
    :param app: Flask instance
    :param message: email message
    :return: nothing
    """
    with app.app_context():
        mail.send(message)
