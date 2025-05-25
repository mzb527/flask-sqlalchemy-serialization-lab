from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# ✅ Customer Model
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # One-to-many relationship with reviews
    reviews = db.relationship('Review', back_populates='customer', cascade="all, delete")

    # Association proxy: Allows easy access to items via reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

# ✅ Item Model
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # One-to-many relationship with reviews
    reviews = db.relationship('Review', back_populates='item', cascade="all, delete")

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

# ✅ Review Model (Links Customers & Items)
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, ForeignKey('items.id'), nullable=False)

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'