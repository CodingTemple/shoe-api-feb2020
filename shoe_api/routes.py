from shoe_api import app,db
from shoe_api.models import User, Product,check_password_hash, product_schema,products_schema
from flask import render_template, request, redirect, url_for, jsonify

from shoe_api.forms import UserForm,LoginForm
from flask_login import login_user, current_user, login_required

import uuid

# Imports for API Token(API KEY)
import jwt
import datetime

from functools import wraps

# Create User Route
@app.route('/user/create', methods = ['GET','POST'])
def create_user():
    form = UserForm()

    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        # Creates a Universally Unique Identifier String
        public_id = str(uuid.uuid4())
        print(email,password,public_id)

        # Add all info to database
        user = User(public_id,email,password)
        db.session.merge(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        print("Form is not valid")
    return render_template('signup.html',form = form)

#Login Route
@app.route('/login', methods=['GET','POST'])
def login():

    loginForm = LoginForm()
    if request.method == 'POST' and loginForm.validate():
        email = loginForm.email.data
        password = loginForm.password.data
        logged_user = User.query.filter(User.email == email).first()
        print(f'login-info: {email}, {password} ')
        if logged_user and check_password_hash(logged_user.password,password):
            login_user(logged_user)
            print(f'current User public_id {current_user.public_id}')
        else:
            return redirect(url_for('login'))
        return redirect(url_for('get_api'))
    return render_template('login.html', form = loginForm)

#Get API Key Route
@app.route('/getapi', methods=['GET'])
def get_api():
    if current_user:
        token = jwt.encode({'public_id': current_user.public_id,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})


# Custom Decorator to validate API KEY Token is passed to a specific route
def token_required(our_flask_function):
    @wraps(our_flask_function) # Copy the contents of the returned function, specifically the parameters
    def decorated(*args,**kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}),401

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            current_user_token = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return our_flask_function(current_user_token, *args,**kwargs)

    return decorated

#@token_required
# def get_products():
    # get all products from database

# ERROR: get_products requires 1 positional argument and 0 found

@app.route('/product', methods=['POST'])
@token_required
def add_product(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    photo = request.json['photo']
    color_way = request.json['color_way']

    new_product = Product(name,description,price,qty,photo,color_way)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get one product
@app.route('/product/<id>', methods = ['GET'])
@token_required
def get_product(current_user_token, id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Get All Products
@app.route('/product', methods = ['GET'])
@token_required
def get_all_products(current_user_token):
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Update Product Route(Endpoint)
@app.route('/product/<id>', methods = ["PUT"])
@token_required
def update_product(current_user_token, id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    photo = request.json['photo']
    color_way = request.json['color_way']

    # Updates to the Database From the request that came in
    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    product.photo = photo
    product.color_way = color_way

    # Commit changes to database
    db.session.commit()

    return product_schema.jsonify(product)

# Delete Route (AKA Delete Endpoint)
@app.route('/product/<id>', methods = ['DELETE'])
@token_required
def delete_product(current_user_toke, id):
    # Look for the product to delete via the id 
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)