from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, InputRequired, NumberRange, ValidationError
from grocery_app.models import ItemCategory, GroceryStore, User
from grocery_app.extensions import bcrypt


def get_stores():
    return GroceryStore.query


class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    # TODO: Add the following fields to the form class:
    # - title - StringField
    # - address - StringField
    # - submit button
    title = StringField('Store Title', validators=[
                        DataRequired(), Length(min=3, max=80)])
    address = StringField('Address', validators=[
                          DataRequired(), Length(min=5, max=200)])
    submit = SubmitField('Submit')


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # TODO: Add the following fields to the form class:
    # - name - StringField
    # - price - FloatField
    # - category - SelectField (specify the 'choices' param)
    # - photo_url - StringField
    # - store - QuerySelectField (specify the `query_factory` param)
    # - submit button
    name = StringField('Item Name', validators=[
                       DataRequired(), Length(min=3, max=80)])
    price = FloatField('Price', validators=[
                       InputRequired(), NumberRange(min=0.01)])
    category = SelectField('Category', choices=ItemCategory.choices())
    photo_url = StringField('Photo URL', validators=[URL()])
    store = QuerySelectField(
        'Store', query_factory=get_stores, allow_blank=False, get_label='title')
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError(
                'No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')
