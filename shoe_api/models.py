from shoe_api import db,app,login_info
from werkzeug.security import generate_password_hash, check_password_hash

# import for flask-marshmallow
from flask_marshmallow import Marshmallow

# import for flask_login Mixins
from flask_login.mixins import UserMixin

# Instantiate Marshmallow Class
ma = Marshmallow(app)



# USER MODEL -- Hold info for the User
@login_info.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(60), unique = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))

    def __init__(self,public_id,email,password):
        self.public_id = public_id
        self.email = email
        self.password = self.password_hash(password)

    def password_hash(self,password):
        return generate_password_hash(password, salt_length=10)

# PRODUCT MODEL -- Hold info for Shoe Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    photo = db.Column(db.String(200))
    color_way = db.Column(db.String(50))

    def __init__(self,name,description,price,qty,photo,color_way):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        self.photo = photo
        self.color_way = color_way

class ProductSchema(ma.Schema):
    class Meta:
        fields = (("id"),'name','description','price','qty','photo','color_way')
   
product_schema = ProductSchema()
products_schema = ProductSchema(many = True)
"""
We will use Marshmallow (Flask-Marshmallow) to create a serialized
version of our class. More plainly, we will create a flattened version of our 
our products class.

The end result will become a schema by which we can create a basic
string respresentation of our products which will look like this:

[{
    "id": 1,
    "name": "Jordan 11",
    "price" : "299.99"
    "description" : "Shoe worn in the last championship run"
    ...
    "photo":"jumpman.jpg"
}]
"""