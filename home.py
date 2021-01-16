from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

# from forms import ProductSearchForm

# from models import Product

# basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
POSTGRES = {
    'user': 'my_user',
    'pw': 'admin',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_user:admin@localhost/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "admin"


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
# products = db.Table('products', db.metadata, autoload=True, autoload_with=db.engine)
db.Model.metadata.reflect(db.engine)
AutoMapModel = automap_base(db.Model)

class User_Reviews(AutoMapModel):
    __table__ = db.Model.metadata.tables['user_reviews']

    def __repr__(self):
        return '<User_Reviews %r>' % self.id
# AutoMapModel.prepare(db.engine, reflect = True)

class Users(AutoMapModel):
    __table__ = db.Model.metadata.tables['users']

    def __repr__(self):
        return '<Users %r>' % self.username
AutoMapModel.prepare(db.engine, reflect = True)

class Products(AutoMapModel):
    __table__ = db.Model.metadata.tables['products']

    def __repr__(self):
        return '<Products %r>' % self.product_name
AutoMapModel.prepare(db.engine, reflect = True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    from product.forms import SearchForm
    form = SearchForm()
    if form.validate_on_submit():
        products = Products.query.filter(Products.product_name.match("%"+form.product.data+"%")).paginate(1,10)
        return render_template('products.html', products=products)
    return render_template('search_product.html', form=form)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/products', methods=['GET', 'POST']) 
def getProducts():
    products = Products.query.paginate(1,10)
    return render_template('products.html', products=products) 

@app.route('/ur_recommendations/<product_name>', methods=['GET', 'POST']) 
def ur_recommendations(product_name):
    products = Products.query.filter_by(product_name=product_name).first().user_review_recommendations
    if not products:
        print("No recommendation available yet.")
    else:
        products = products[1:-1]
        products = products.replace("'","")
        products = products.strip()
        products_list = products.split(", ")
        while ("" in products_list):
            products_list.remove("")
        print(products_list)
        products =[]
        for product in products_list:
            p = Products.query.filter_by(product_name=product).first()
            products.append(p)
        return render_template('products_list.html', products=products)    

@app.route('/product/<product_name>')
def product(product_name):
    product = Products.query.filter_by(product_name=product_name).first()
    print(product)
    return render_template('product.html', product=product)    

@app.route('/add_product', methods=['GET', 'POST'])
def addProduct():
    from product.forms import AddProductForm
    form = AddProductForm()
    if form.validate_on_submit():
        product = Products(product_name =form.product_name.data, brand=form.brand.data, categories = form.categories.data, price = form.price.data, image_url = form.image_url.data)
        db.session.add(product)
        db.session.commit()
        flash('You have added a product.')
        return render_template('search_product.html', form=form)
    return render_template('add_product.html', form=form)