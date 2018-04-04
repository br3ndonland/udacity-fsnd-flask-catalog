#!/usr/bin/env python3

"""
Udacity Full Stack Web Developer Nanodegree program (FSND)
Project 4. Flask Item Catalog App

application.py
~~~~~~~~~~~~~~

This file contains the main Flask application code.
"""

# Import SQLAlchemy modules for database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# Import OAuth modules for user authentication
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

# Import Flask modules from flask library
from flask import Flask, flash, jsonify, make_response, redirect
from flask import render_template, request, url_for
from flask import session as login_session

# Other modules
import json
import random
import requests
import string


# Create an instance of class Flask.
# Each time the application runs, a special variable 'name' is defined.
app = Flask(__name__)


# Connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


"""
App route functions
~~~~~~~~~~~~~~~~~~~
"""


@app.route('/')
def home():
    """App route function for the homepage."""

    # Query database with SQLAlchemy to show all categories
    categories = (session.query(Category)
                  .order_by(Category.name)
                  .all())
    # Query database with SQLAlchemy to show most recent ten items
    recent_items = (session.query(Item)
                    .order_by(Item.date_created.desc())
                    .limit(10))

    # Render webpage
    return render_template('index.html',
                           categories=categories,
                           recent_items=recent_items)


@app.route('/<string:category>')
def show_category(category):
    """App route function to display all items in a specific category."""

    # Query database with SQLAlchemy to show all categories
    categories = (session.query(Category)
                  .order_by(Category.name)
                  .all())
    # Query database with SQLAlchemy to show selected category and items
    category = (session.query(Category)
                .filter_by(name=category)
                .one())
    category_items = (session.query(Item)
                      .filter_by(category_id=category.id)
                      .order_by(Item.name)
                      .all())
    category_items_count = (session.query(Item)
                            .filter_by(category_id=category.id)
                            .count())

    # Render webpage
    return render_template('show_category.html',
                           categories=categories,
                           category_name=category.name,
                           category_items=category_items,
                           category_items_count=category_items_count)


@app.route('/<string:category>/<string:item>')
def show_item(category, item):
    """App route function to display an item."""

    # Query database with SQLAlchemy to show selected category and item
    category = (session.query(Category)
                .filter_by(name=category)
                .one())
    item = (session.query(Item)
            .filter_by(name=item.replace('-', ' '), category_id=category.id)
            .one())

    # Render webpage
    return render_template('show_item.html',
                           item=item,
                           category=category)


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    """App route function to create categories with POST requests."""

    # Verify user is logged in. If not, redirect to login page.
    if 'username' not in login_session:
        flash('Please log in.')
        return redirect('/login')

    if request.method == 'POST':
        # Flash messages for incomplete item info
        if not request.form['name']:
            flash('Please add category name')
            return redirect(url_for('add_category'))
        if not request.form['description']:
            flash('Please add a description')
            return redirect(url_for('add_category'))

        # If user is logged in, and all info provided, add item
        new_category = Category(name=request.form['name'],
                                user_id=login_session['user_id'])
        session.add(new_category)
        session.commit()

        # Return to page for category
        return redirect(url_for('show_category'))

    else:
        # Get all categories
        categories = session.query(Category).all()
        # Render webpage
        return render_template('add_category.html', categories=categories)


@app.route('/add-item', methods=['GET', 'POST'])
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
        # Render webpage
        return render_template('add_item.html', categories=categories)


@app.route('/<string:category>/<string:category_item>/edit',
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
        # Render webpage
        return render_template('edit_item.html',
                               categories=categories,
                               item=item)


@app.route('/<string:category>/<string:category_item>/delete',
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
        # Render webpage
        return render_template('delete_item.html', item=item)


"""
JSON functions
~~~~~~~~~~~~~~
"""


@app.route('/json')
def catalog_json():
    """App route function to provide catalog data in JSON format."""

    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/<string:category>/json`')
def show_category_json(category_id):
    """App route function to provide category data in JSON format."""

    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[items.serialize for item in items])


@app.route('/<string:category>/<string:category_item>/json')
def show_item_json(category_id, item_id):
    """App route function to provide item data in JSON format."""

    item = session.query(Item).filter_by(id=item_id).first()
    return jsonify(item=[item.serialize])


"""
Login functions
~~~~~~~~~~~~~~~
"""

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


# Login page
@app.route('/login')
def login():
    """App route function to log in and generate token."""

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # Render webpage
    return render_template('login.html', STATE=state)


# GConnect login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """App route function for Google GConnect login."""

    # Confirm that client and server tokens match
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    resp = requests.get(url=url)
    result = json.loads(resp.text)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for the user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Create new user if user does not already exist
    user = session.query(User).filter_by(email=data['email']).first()
    if user:
        print('{} already exists.'.format(user.email))
    else:
        new_user = User(name=data['name'], email=data['email'],
            picture_url=data['picture'])
        session.add(new_user)
        session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    flash('Logged in as {}'.format(login_session['username']))
    print('Logged in as {}'.format(login_session['username']))
    print('Done!')
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """App route function to disconnect from Google login."""

    try:
        access_token = login_session['credentials']
    except KeyError:
        flash('Failed to get access token')
        return redirect('/')

    print('GDisconnect access token is {}'.format(access_token))
    print('User name is {}'.format(login_session['username']))
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
        % login_session['credentials'])
    print(url)
    resp = requests.get(url=url)
    print('Result is {}'.format(resp))

    del login_session['credentials']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    flash('Successfully logged out.')

    return redirect('/')


# If this file is called as a standalone program:
if __name__ == '__main__':
    # Run the Flask app on port 8000 and enable debugging
    app.run(host='0.0.0.0', port=8000, debug=True)
    app.secret_key = 'super_secret_key'
