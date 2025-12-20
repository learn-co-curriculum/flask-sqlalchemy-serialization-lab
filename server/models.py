from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # a customer can have many reviews
    reviews = db.relationship('Review', back_populates='customer')

    # association proxy to get items through reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # an item can have many reviews
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'



class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    # foreign keys connect reviews to customers and items
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # each review belongs to one customer
    customer = db.relationship('Customer', back_populates='reviews')

    # each review belongs to one item
    item = db.relationship('Item', back_populates='reviews')


class CustomerSchema(Schema):
    id = fields.Int()
    name = fields.String()

    # include reviews, but exclude anything that causes recursion
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('customer', 'item'))


class ItemSchema(Schema):
    id = fields.Int()
    name = fields.String()
    price = fields.Float()

    # include reviews, but exclude anything that causes recursion
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('customer', 'item'))


class ReviewSchema(Schema):
    id = fields.Int()
    comment = fields.String()

    # include customer, exclude items and reviews (to avoid recursion)
    customer = fields.Nested('CustomerSchema', exclude=('reviews',))

    # include item, exclude reviews and customers (to avoid recursion)
    item = fields.Nested('ItemSchema', exclude=('reviews',))
