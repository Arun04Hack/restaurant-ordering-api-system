# Restaurant Ordering API

A simple restaurant ordering backend built with FastAPI, SQLAlchemy, SQLite, and Pydantic.

## Overview

This project was built to learn the fundamentals of backend development with FastAPI and relational databases. It implements a basic restaurant ordering workflow where dishes can be categorized, customers can register, and orders can be placed.

## Features

* Create and manage categories
* Create dishes and assign categories
* Register customers
* View dish information
* View category information
* View customer information
* Place orders
* Track order status

## Database Relationships

### Category ↔ Dish

Many-to-Many relationship using an association table.

### Customer → Order

One customer can have multiple orders.

### Order → OrderItem

One order can contain multiple order items.

### Dish → OrderItem

A dish can appear in multiple order items.

## Tech Stack

* FastAPI
* SQLAlchemy ORM
* SQLite
* Pydantic

## Learning Objectives

This project helped me practice:

* FastAPI routing
* Request and response handling
* Dependency injection
* Database modeling
* SQLAlchemy relationships
* Data validation with Pydantic
* CRUD operations
* Error handling

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Create database tables:

```bash
python create_db.py
```

Start the server:

```bash
fastapi dev
```

Open:

http://127.0.0.1:8000/docs

to test the API through Swagger UI.
