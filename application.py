#!/usr/bin/env python3

# Udacity Full Stack Web Developer Nanodegree program (FSND)
# Part 03. Backend
# Project 02. Flask Item Catalog App
# Flask application code

# Import SQLAlchemy modules for database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# Import OAuth modules for user authentication
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

# Import Flask modules from flask library
from flask import Flask
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask import session as login_session

# Other modules
import random
import string
import json
import requests


# Create an instance of class Flask.
# Each time the application runs, a special variable 'name' is defined.
app = Flask(__name__)


# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Functions for establishing login session and user info
CLIENT_ID = json.loads(open('client_secrets.json', 'r')
    .read())['web']['client_id']


def create_user(login_session):
    """Create new user based on login info."""
    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    photo=login_session['photo'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_id(user_id):
    """Get user ID."""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_email(email):
    """Get user email."""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


# Decorators to wrap each function inside Flask's app.route() function

# CRUD: Read homepage and catalog page
@app.route('/')
@app.route('/catalog')
def home():
    """App route function for the homepage."""
    categories = session.query(Category).all()
    recent_items = (session.query(Item)
        .order_by(Item.date_created.desc())
        .limit(10)
        .all())
    return render_template('index.html',
                           categories=categories,
                           recent_items=recent_items)


@app.route('/catalog/json')
def home_json():
    """App route function to provide homepage data in JSON format."""
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


# CRUD: Read pages for categories
@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items')
def show_category(category_id):
    """App route function to display all items in a specific category."""
    # Get category info
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).first()
    category_name = category.name

    # Get all items in a specific category
    category_items = session.query(Item).filter_by(category_id).all()

    # Get count of category items
    category_items_count = session.query(Item).filter_by(category_id).count()

    return render_template('category.html',
                           categories=categories,
                           category_items=category_items,
                           category_name=category_name,
                           category_items_count=category_items_count)


@app.route('/catalog/<int:category_id>/json`')
@app.route('/catalog/<int:category_id>/items/json')
def show_category_json(category_id):
    """App route function to provide category data in JSON format."""
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[items.serialize for item in items])


# CRUD: Read specific item
@app.route('/catalog/<int:category_id>/items/<int:item_id>')
def show_item(category_id, item_id):
    """App route function to display an item."""
    item = session.query(Item).filter_by(id=item_id).first()
    item_creator = get_user_id(item.user_id)
    return render_template('item.html', item=item, creator=item_creator)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/json')
def show_item_json(category_id, item_id):
    """App route function to provide item data in JSON format."""
    item = session.query(Item).filter_by(id=item_id).first()
    return jsonify(item=[item.serialize])


# CRUD: Create an item
@app.route('/catalog/add', methods=['GET', 'POST'])
def add_item():
    """App route function to create items with POST requests."""
    # Verify user is logged in. If not, redirect to login page.
    if 'username' not in login_session:
        flash('Please log in.')
        return redirect('/login')

    if request.method == 'POST':
        # Flash messages for incomplete item info
        if not request.form['name']:
            flash('Please add item name')
            return redirect(url_for('add_item'))
        if not request.form['description']:
            flash('Please add a description')
            return redirect(url_for('add_item'))

        # If user is logged in, and all info provided, add item
        new_item = Item(name=request.form['name'],
                        description=request.form['description'],
                        category_id=request.form['category'],
                        user_id=login_session['user_id'])
        session.add(new_item)
        session.commit()

        # Return to page for the item's category
        return redirect(url_for('show_category'))

    else:
        # Get all categories
        categories = session.query(Category).all()

        return render_template('add_item.html', categories=categories)


# CRUD: Update/edit an item
@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def edit_item(category_id, item_id):
    """App route function to edit an item."""
    # Verify user is logged in. If not, redirect to login page.
    if 'username' not in login_session:
        flash('Please log in.')
        return redirect('/login')

    # Get item to edit
    item = session.query(Item).filter_by(id=item_id).first()

    # Only allow item creator to edit. If not, redirect to login.
    item_category = session.query(Category).filter_by(id=item_id).first()
    item_creator = get_user_id(Item.user_id)
    if item_creator.id != login_session['user_id']:
        return redirect('/login')

    # Get categories
    categories = session.query(Category).all()

    # Show item to edit, or redirect
    if request.method == 'POST':
        if request.form['name']:
            Item.name = request.form['name']
        if request.form['description']:
            Item.description = request.form['description']
        if request.form['category']:
            Item.category_id = request.form['category']
        return redirect(url_for('show_item',
                                category_id=item_category.category_id,
                                item_id=item.id))
    else:
        return render_template('edit_item.html',
                               categories=categories,
                               item=item)


# CRUD: Delete an item
@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def delete_item(category_id, item_id):
    """App route function to delete an item."""
    # Verify user is logged in. If not, redirect to login page.
    if 'username' not in login_session:
        flash('Please log in.')
        return redirect('/login')

    # Get item to edit
    item = session.query(Item).filter_by(id=item_id).first()

    # Only allow item creator to edit. If not, redirect to login.
    item_category = session.query(Category).filter_by(id=item_id).first()
    item_creator = get_user_id(Item.user_id)
    if item_creator.id != login_session['user_id']:
        return redirect('/login')

    # Show item to delete, or redirect
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('show_category',
                                category_id=item_category.category_id))
    else:
        return render_template('delete_item.html', item=item)


# If this file is called as a standalone program:
if __name__ == '__main__':
    # Run the Flask app on port 8000 and enable debugging
    app.run(host='0.0.0.0', port=8000, debug=True)
