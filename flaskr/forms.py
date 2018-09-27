from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flaskr.models import User
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    """
    create login form from flaskform object
    """
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember me?"))
    submit = SubmitField(_l('Sign in'))


class RegistrationForm(FlaskForm):
    """
    create registration form from flaskform object
    """
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password: StringField = StringField(_l('Password'), validators=[DataRequired()])
    password2 = StringField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    @staticmethod
    def validate_username(username):
        """
        validate username is unique
        :param username: expects string
        :return: none
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please choose a different username.'))

    @staticmethod
    def validate_email(email):
        """
        validate email is unique
        :param email: expects string
        :return: none
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address'))


class EditProfileForm(FlaskForm):
    """
    create Edit Profile form from flask form object
    """
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About Me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """
        validate that username changes are to a unique username
        :param username: expects string
        :return: none
        """
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))


class PostForm(FlaskForm):
    """
    create a form to submit blog posts from flask form object
    """
    post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))


class ResetPasswordRequestForm(FlaskForm):
    """
    create reset password request form
    """
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request password reset'))


class ResetPasswordForm(FlaskForm):
    """
    create password reset form
    """
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset password'))
