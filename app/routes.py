from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy
# from app.forms import SearchForm

from app import app,db
from app.models import Users, Products, User_Reviews

# bootstrap = Bootstrap(app)

# products = db.Table('products', db.metadata, autoload=True, autoload_with=db.engine)


@app.route('/', methods=['GET', 'POST'])
def index():
    from app.forms import SearchForm
    form = SearchForm()
    if form.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        search_input = (form.product.data).title()
        pagination = Products.query.filter(Products.product_name.contains(search_input)).paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
        products = pagination.items
        ## OLD PRODUCT QUERY
        # products = Products.query.filter(Products.product_name.match("%"+form.product.data+"%")).paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
        ## old render
        # return render_template('products.html', title='Home',products=products, pagination=pagination)
        return redirect(url_for('.getProducts',search_input = search_input))
    return render_template('search_product.html', form=form)

@app.route('/<brand_name>',methods =['GET'])
def brand_list(brand_name):
    products = Products.query.filter_by(brand=brand_name).all()
    page = request.args.get('page', 1, type=int)
    pagination = Products.query.filter_by(brand=brand_name).paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
    products = pagination.items
    print ("#### products at page:", page, ": ", products)
    if products == []:
        return render_template('404.html', code=404)
    return render_template('products.html', title='Product list for "'+brand_name+'"' ,products=products, pagination=pagination, pagiType = 1, brand_name = brand_name)

@app.route('/brand_list')
def getAllBrands():
    brands = Products.query.all()
    all_brands = []
    for brand in brands:
        all_brands.append(brand.brand)
    all_brands = list(set(all_brands))
    all_brands = sorted(all_brands)
    if all_brands == []:
        return render_template('404.html', code=404)
    return render_template('brands.html', title='Brand List', brands = all_brands)

@app.route('/product_type/skin_care')
def getAllSkinCare():
    products = Products.query.filter(Products.categories.contains('Skin Care')).all()
    page = request.args.get('page', 1, type=int)
    pagination = Products.query.filter(Products.categories.contains('Skin Care')).paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
    products = pagination.items
    return render_template('products.html', title='Skin Care Products',products=products, pagination=pagination, pagiType =2)

@app.route('/product_type/make_up')
def getAllMakeup():
    products = Products.query.filter(Products.categories.contains('Make Up')).all()
    page = request.args.get('page', 1, type=int)
    pagination = Products.query.filter(Products.categories.contains('Make Up')).paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
    products = pagination.items
    return render_template('products.html', title='MakeUp Products',products=products, pagination=pagination, pagiType =3)
    

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# @app.route('/products_default') 
# def getProduct():
#     print("RUNNNNNNNNNNNNNNNNNNNNINNNNNNNNNG")
#     page = request.args.get('page', 1, type=int)
#     pagination = Products.query.paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
#     products = pagination.items
#     # products = Products.query.paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
#     return render_template('products.html', title='Product',products=products, pagination=pagination) 

@app.route('/products/<search_input>', methods=['GET', 'POST']) 
def getProducts(search_input):
    page = request.args.get('page', 1, type=int)
    search_input = search_input
    pagination = Products.query.filter(Products.product_name.contains(search_input)).paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
    products = pagination.items
    if products == []:
        return render_template('no_search_result.html', code=200)
    return render_template('products.html', title='Search result for "'+search_input+'"',products=products, pagination=pagination, pagiType =4, search_input = search_input) 

@app.route('/ur_recommendations/<product_name>', methods=['GET', 'POST']) 
def ur_recommendations(product_name):
    products = Products.query.filter_by(product_name=product_name).first().user_review_recommendations
    if not products:
        print("No recommendation available yet.")
    else:
        # products = products[1:-1]
        # products = products.replace("'","")
        # products = products.strip()
        products_list = products.split(", ")
        while ("" in products_list):
            products_list.remove("")
        print(products_list)
        products =[]
        for product in products_list:
            p = Products.query.filter_by(product_name=product).first()
        ## TEST CASE
        # p = Products.query.filter_by(product_name='Cosrx AC Collection Calming Liquid Mild 125ml').first()
            products.append(p)
        return render_template('products_list.html', products=products, title = "User Reviews Product Recommendations")

@app.route('/rating_recommendations/<product_name>', methods=['GET', 'POST']) 
def rating_recommendations(product_name):
    products = Products.query.filter_by(product_name=product_name).first().rating_recommendations
    if not products:
        print("No recommendation available yet.")
    else:
        products_list = products.split(", ")
        while ("" in products_list):
            products_list.remove("")
        print(products_list)
        products =[]
        for product in products_list:
            p = Products.query.filter_by(product_name=product).first()
        ## TEST CASE
        # p = Products.query.filter_by(product_name='Cosrx AC Collection Calming Liquid Mild 125ml').first()
            products.append(p)
        return render_template('products_list.html', products=products, title ="Rating Product Recommendation")    

@app.route('/product/<product_name>')
def product(product_name):
    product = Products.query.filter_by(product_name=product_name).first()
    print(product)
    hasReview = True
    reviews = User_Reviews.query.filter_by(product_name=product_name).all()
    num_reviews = len(reviews)
    ### KEYWORD processing
    keywords = product.keywords
    if keywords: 
        keywords = product.keywords[1:-1].replace("'","").strip().replace('"','')
        keywords = keywords.split(",")
        while ("" in keywords):
            keywords.remove("")
        ### keywords reviews only
        # k_review =[]
        # keys = keywords[1:-1].replace('"','').replace(" ",",").split(",")
        # for k in keys:
        #     k_review.append(User_Reviews.query.filter_by(product_name=product_name).filter(User_Reviews.text.contains(k)).all())
        
        # review based on ratings
        if reviews != []:
            reviews_rating = []
            for review in range(5):
                reviews_rating.append(User_Reviews.query.filter_by(product_name=product_name, sentiment_score=str(review+1)).all())
        else:
            hasReview = False 
    else:
        keywords = ["No discussion yet..."]
        reviews = ["No review yet..."]
        reviews_rating = 0
        hasReview = False
    page = request.args.get('page', 1, type=int)
    pagination = User_Reviews.query.filter_by(product_name=product_name).paginate(page,app.config['PRODUCTS_PER_PAGE'], False)
    reviews = pagination.items    
    print(product)
    return render_template('product.html', product=product, reviews = reviews, reviews_rating=reviews_rating, pagination = pagination, hasReview = hasReview, num_reviews= num_reviews,keywords = keywords, isFilter = False)    

@app.route('/product/<product_name>/<keyword>')
def product_review_filter(product_name, keyword):
    product = Products.query.filter_by(product_name=product_name).first()
    num_reviews = len(User_Reviews.query.filter_by(product_name=product_name).all())
    hasReview= True
    ### KEYWORD processing
    keywords = product.keywords
    if keywords: 
        keywords = product.keywords[1:-1].replace("'","").strip().replace('"','')
        keywords = keywords.split(",")
        while ("" in keywords):
            keywords.remove("")

    k_review =[]
    # keyword = keywords[]
    if keyword: 
        keys = keyword.split(" ")
        for k in keys:
            k_review2 = User_Reviews.query.filter_by(product_name=product_name).filter(User_Reviews.text.contains(k)).all()
        k_review = list(k_review)
        k_review.extend(x for x in k_review2 if x not in k_review)
        # review based on ratings
        if k_review != []:
            reviews_rating = []
            for review in range(5):
                reviews_rating.append(User_Reviews.query.filter_by(product_name=product_name, sentiment_score=str(review+1)).filter(User_Reviews.text.contains(k)).all())
        else:
            hasReview = False 
    else:
        keywords = ["No discussion yet..."]
        k_review = ["No review yet..."]
        reviews_rating = 0
        hasReview = False
    page2 = request.args.get('page', 1, type=int)
    pagination2 = User_Reviews.query.filter_by(product_name=product_name).filter(User_Reviews.text.contains(k)).paginate(page2,5, False)
    reviews = pagination2.items    
    print(product)
    return render_template('product.html', product=product, reviews = reviews, reviews_rating=reviews_rating, pagination = pagination2, hasReview = hasReview, num_reviews= num_reviews,keywords = keywords, isFilter = True, keyword = keyword) 

@app.route('/add_product', methods=['GET', 'POST'])
def addProduct():
    from product.forms import AddProductForm
    form = AddProductForm()
    if form.validate_on_submit():
        product = Products(product_name =form.product_name.data, brand=form.brand.data, categories = form.categories.data, price = form.price.data, image_url = form.image_url.data)
        db.session.add(product)
        db.session.commit()
        db.session.close()
        flash('You have added a product.')
        return render_template('search_product.html', form=form)
    return render_template('add_product.html', form=form)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     from product.forms import SearchForm
#     form = SearchForm()
#     if form.validate_on_submit():
#         products = Products.query.filter(Products.product_name.match("%"+form.product.data+"%")).paginate(1,10)
#         return render_template('products.html', products=products)
#     return render_template('search_product.html', form=form)

@app.route('/test')
def loadTest():
    return render_template('test.html')

# @app.route('/ranking')
# def loadRank():
#     return render_template('ranking.html')