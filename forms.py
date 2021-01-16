# from home import Users 
from wtforms import Form, StringField, SelectField, BooleanField, SubmitField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from home import Products


class AddProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(1, 60)])
    brand = StringField('Brand', validators=[DataRequired(), Length(1, 60)])
    categories = SelectField('Category', choices=[('Skincare','Skincare'),('Makeup','Makeup')])
    price = IntegerField('Price in (RM)')
    image_url = StringField('Image address', validators=[DataRequired()])
    submit = SubmitField('Submit')    

    def validate_product(self, field):
        if Products.get.fiter_by(product_name=field.data).first():
            raise ValidationError ('Product already exists.')

class SearchForm(FlaskForm):
    product = StringField('Product Search', validators=[DataRequired(), Length(1,64)])
    submit = SubmitField('Search')
 