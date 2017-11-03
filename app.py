from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://modeling:blog@localhost/ModelDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# nigggA

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1000), index=True)
    image_reference = db.Column(db.String(1000), index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    children = db.relationship("Category", backref=db.backref('subCategories', remote_side=[id]))
    services = db.relationship('Service',backref='category_Services', lazy='dynamic')

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1000), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    listings = db.relationship('Listing', backref='service_Listings', lazy='dynamic')


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(124))
    phoneNumber = db.Column(db.Integer)
    description = db.Column(db.String(1000), index=True)
    price = db.Column(db.Float)
    discountPercent = db.Column(db.Float)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    freelancer_id = db.Column(db.Integer, db.ForeignKey('freelancer.id'))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Number = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    phoneNumber = db.Column(db.Integer)




class Freelancer(User):
    __tablename__ = 'freelancer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    listings = db.relationship('Listing', backref='freelancerListings', lazy='dynamic')


    __mapper_args__ = {
        'polymorphic_identity':'freelancer',
    }

class Customer(User):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    cart = db.relationship("Cart",  uselist=False, back_populates="customer")


    __mapper_args__ = {
        'polymorphic_identity':'customer',
    }

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship("Customer", back_populates="cart")
    listings = db.relationship('Listing', backref='cart_Listings', lazy='dynamic')




@app.route('/')
def index():
    return '<h1> This is the home page!</h1>'

if __name__ == '__main__':
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()
