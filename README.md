# Flask SQLAlchemy Serialization Lab

## Overview

This project demonstrates how to use Flask, SQLAlchemy, Association Proxies, and Marshmallow serialization to model and serialize related data.

The application includes three models:

* Customer
* Item
* Review

Customers can leave reviews on items, creating relationships between all three models.

---

## Features

* SQLAlchemy ORM models
* One-to-many relationships
* Foreign key constraints
* Association Proxy implementation
* Marshmallow serialization schemas
* Nested serialization without recursive loops
* Automated testing with pytest

---

## Project Structure

```text
server/
├── app.py
├── models.py
├── seed.py
├── conftest.py
└── testing/
    ├── review_test.py
    ├── association_proxy_test.py
    └── serialization_test.py
```

---

## Models

### Customer

Represents a customer who can write reviews.

Attributes:

* id
* name

Relationships:

* reviews
* items (via association proxy)

### Item

Represents a product that can receive reviews.

Attributes:

* id
* name
* price

Relationships:

* reviews

### Review

Represents a review connecting a customer and an item.

Attributes:

* id
* comment
* customer_id
* item_id

Relationships:

* customer
* item

---

## Association Proxy

Customers can access reviewed items directly through:

```python
customer.items
```

This is implemented using SQLAlchemy's Association Proxy feature.

---

## Serialization

Marshmallow schemas are used to serialize models into dictionaries.

### CustomerSchema

Serializes:

* id
* name
* reviews

### ItemSchema

Serializes:

* id
* name
* price
* reviews

### ReviewSchema

Serializes:

* id
* comment
* customer
* item

Nested serialization is configured to prevent infinite recursion.

---

## Installation

Create and activate your virtual environment:

```bash
pipenv install
pipenv shell
```

Install dependencies:

```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate marshmallow pytest
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run individual test files:

```bash
pytest testing/review_test.py
pytest testing/association_proxy_test.py
pytest testing/serialization_test.py
```

---

## Example Seed Data

The seed file creates:

### Customers

* Tal Yuri
* Raha Rosario
* Luca Mahan

### Items

* Laptop Backpack
* Insulated Coffee Mug
* 6 Foot HDMI Cable

### Reviews

Examples include:

* "love this backpack!"
* "coffee stays hot for hours!"
* "best coffee mug ever!"

---

## Learning Objectives

* Build SQLAlchemy relationships
* Use foreign keys correctly
* Implement association proxies
* Serialize related objects with Marshmallow
* Prevent recursive serialization issues
* Write and pass automated tests

---

## Author

Steven Rouse


