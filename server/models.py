from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Flask-SQLAlchemy uses this object to create tables and manage database queries.
db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    """A person who reviews items in the store."""

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # A customer can write many reviews, and can reach reviewed items through them.
    reviews = db.relationship('Review', back_populates='customer')
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model):
    """A product that customers can review."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Reviews connect each item to the customers who reviewed it.
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model):
    """A customer's comment about one item."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # These relationships let a review point back to its customer and item.
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')


class CustomerSchema(Schema):
    """Convert customers and their reviews into JSON-friendly dictionaries."""

    id = fields.Int()
    name = fields.Str()
    # Excluding the customer here stops a review from nesting this customer again.
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('customer',))


class ItemSchema(Schema):
    """Convert items and their reviews into JSON-friendly dictionaries."""

    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    # Excluding the item here stops a review from nesting this item again.
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('item',))


class ReviewSchema(Schema):
    """Convert a review with its related customer and item."""

    id = fields.Int()
    comment = fields.Str()
    # Nested customer and item schemas leave their reviews out to prevent loops.
    customer = fields.Nested(CustomerSchema, exclude=('reviews',))
    item = fields.Nested(ItemSchema, exclude=('reviews',))
