from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, InputRequired, NumberRange
from grocery_app.models import ItemCategory, GroceryStore


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
