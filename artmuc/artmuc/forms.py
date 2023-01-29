from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from artmuc.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    artist_key = StringField("Artist Key, Leave Blank If You're A Customer", validators=[Length(min=0, max=384)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username Is Taken. Please Choose A Different One.')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That Email Is Taken. Please Choose A Different One.')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['png', 'jpg'])])
    biography = TextAreaField('Biography', validators=[Length(min=0, max=250)])
    submit = SubmitField('Update Profile')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username Is Taken. Please Choose A Different One.')
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That Email Is Taken. Please Choose A Different One.')
class UpdateCustomerAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    country = StringField('Country', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    zip = StringField('Postal Code', validators=[DataRequired()])
    submit = SubmitField('Update Payment Information')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username Is Taken. Please Choose A Different One.')

class PostForm(FlaskForm):
    product_name = StringField('Title', validators=[DataRequired()])
    product_description = TextAreaField('Description', validators=[DataRequired(), Length(min=5, max=250)])
    picture = FileField('Upload A Picture Of Your Product', validators=[DataRequired(), FileAllowed(['png', 'jpg'])])
    product_price = StringField('Price In Euros', validators=[DataRequired()])
    submit = SubmitField('List For Sale')
