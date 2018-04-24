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
from database_setup import Base, Categories, Items, Users

# Import Flask modules from flask library
from flask import Flask, flash, jsonify, make_response, redirect
from flask import render_template, request, url_for
from flask import session as login_session

# Import authentication modules
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

# Import other modules
import json
import random
import requests
import string


"""
Initialize app and database
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create an instance of class Flask.
The instance must be defined at the top of the program to create app routes.
Each time the application runs, a special variable 'name' is defined.

Connect to database and establish database session.
"""

app = Flask(__name__)
APPLICATION_NAME = 'Flask Catalog'
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


"""
App route functions available prior to login
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@app.route('/')
def home():
    """App route function for the homepage."""
    login_status = None
    if 'user_id' in login_session:
        login_status = True
    # Query database with SQLAlchemy to show all categories
    categories = (session.query(Categories)
                  .order_by(Categories.name)
                  .all())
    # Query database with SQLAlchemy to show most recent ten items
    recent_items = (session.query(Items)
                    .order_by(Items.date_created.desc())
                    .limit(10))
    # Render webpage
    return render_template('index.html',
                           categories=categories,
                           recent_items=recent_items,
                           login_status=login_status)


@app.route('/json')
def catalog_json():
    """App route function to provide catalog data in JSON format."""
    all_categories = (session.query(Categories).all())
    all_items = (session.query(Items).all())
    return jsonify(categories=([all_categories.serialize
                                for all_categories in all_categories]),
                   items=([all_items.serialize
                           for all_items in all_items]))


@app.route('/<string:category>')
def show_category(category):
    """App route function to display all items in a specific category."""
    login_status = None
    if 'user_id' in login_session:
        login_status = True
    # Query database with SQLAlchemy to show all categories
    categories = (session.query(Categories)
                  .order_by(Categories.name)
                  .all())
    # Query database with SQLAlchemy to show selected category and items
    category = (session.query(Categories)
                .filter_by(name=category.replace('-', ' '))
                .one())
    category_items = (session.query(Items)
                      .filter_by(category_id=category.id)
                      .order_by(Items.name)
                      .all())
    category_items_count = (session.query(Items)
                            .filter_by(category_id=category.id)
                            .count())
    # Render webpage
    return render_template('show_category.html',
                           categories=categories,
                           category_name=category.name,
                           category_items=category_items,
                           category_items_count=category_items_count,
                           login_status=login_status)


@app.route('/<string:category>/json')
def show_category_json(category):
    """App route function to provide category data in JSON format."""
    category = (session.query(Categories)
                .filter_by(name=category.replace('-', ' '))
                .one())
    category_items = (session.query(Items)
                      .filter_by(category_id=category.id)
                      .order_by(Items.name)
                      .all())
    return jsonify(category=[category.serialize],
                   items=([category_items.serialize
                           for category_items in category_items]))


@app.route('/<string:category>/<string:item>')
def show_item(category, item):
    """App route function to display an item."""
    login_status = None
    if 'user_id' in login_session:
        login_status = True
    # Query database with SQLAlchemy to show selected category and item
    category = (session.query(Categories)
                .filter_by(name=category)
                .one())
    item = (session.query(Items)
            .filter_by(name=item.replace('-', ' '), category_id=category.id)
            .one())
    # Render webpage
    return render_template('show_item.html',
                           item=item,
                           category=category,
                           login_status=login_status)


@app.route('/<string:category>/<string:item>/json')
def show_item_json(category, item):
    """App route function to provide item data in JSON format."""
    category = (session.query(Categories)
                .filter_by(name=category)
                .one())
    item = (session.query(Items)
            .filter_by(name=item.replace('-', ' '))
            .one())
    return jsonify(item=[item.serialize])


"""
Login functions
~~~~~~~~~~~~~~~
"""

# Obtain credentials from JSON file
CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
CLIENT_SECRET = json.loads(open('client_secrets.json', 'r')
                           .read())['web']['client_secret']
redirect_uris = json.loads(open('client_secrets.json', 'r')
                           .read())['web']['redirect_uris']


@app.route('/login')
def login():
    """App route function to log in and generate token."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # Render webpage
    return render_template('login.html',
                           CLIENT_ID=CLIENT_ID,
                           STATE=state)


# GConnect login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """App route function for Google Sign-In."""
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
    # Verify that the access token is valid in general.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
           .format(access_token))
    resp = requests.get(url=url)
    result = json.loads(resp.text)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for the user.
    user_id = credentials.id_token['sub']
    print('Google User ID is {}.'.format(user_id))
    print('Result from Google access token is {}.'.format(result))
    if result['user_id'] != user_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print('Access token valid for the user.')
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_user_id = login_session.get('user_id')
    if stored_credentials is not None and user_id == stored_user_id:
        print('User is already connected.')
        response = make_response(json.dumps(
            'Users is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print('Access token valid for this app.')
    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.token_uri
    login_session['user_id'] = user_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['name'] = data['name']
    login_session['email'] = data['email']
    # Verify contents of login_session
    print('login_session object currently contains: {}'.format(login_session))
    # Check database for user
    user = session.query(Users).filter_by(email=data['email']).first()
    if user:
        print('{} already exists.'.format(data['email']))
    # Create new user if user does not already exist
    else:
        new_user = Users(
            name=login_session['name'], email=login_session['email'], user_id=login_session['user_id'])
        session.add(new_user)
        session.commit()
        print('New user {} added to database.'.format(data['email']))
    output = ''
    output += '<h3 class="font-weight-light">Welcome, '
    output += login_session['name']
    output += '!</h3>'
    output += '<img src="'
    flash('Logged in as {}'.format(login_session['email']))
    print('Logged in as {}'.format(login_session['email']))
    print('Done!')
    return output


def create_user(login_session):
    """Create new user based on login info."""
    new_user = Users(name=login_session['name'],
                     email=login_session['email'],
                     user_id=login_session['user_id'])
    session.add(new_user)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def get_user_email(email):
    """Get user email."""
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.email
    except Exception:
        return None


def get_user_id(user_id):
    """Get user id."""
    try:
        user = session.query(Users).filter_by(user_id=user_id).one()
        return user.user_id
    except Exception:
        return None


"""
App route functions available after login
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    """App route function to create categories with POST requests."""
    # Verify user is logged in. If not, redirect to login page.
    if 'user_id' not in login_session:
        flash('Please log in.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Flash messages for incomplete item info
        if not request.form['name']:
            flash('Please add category name')
            return redirect(url_for('add_category'))
        if not request.form['description']:
            flash('Please add a description')
            return redirect(url_for('add_category'))
        # If user is logged in, and all info provided, add item
        new_category = Categories(name=request.form['name'],
                                  email=login_session['email'])
        session.add(new_category)
        session.commit()
        # Return to homepage
        return redirect(url_for('home'))
    else:
        # Get all categories
        categories = session.query(Categories).all()
        # Render webpage
        return render_template('add_category.html', categories=categories)


@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    """App route function to create items with POST requests."""
    # Verify user is logged in. If not, redirect to login page.
    if 'user_id' not in login_session:
        flash('Please log in.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Flash messages for incomplete item info
        if not request.form['name']:
            flash('Please add item name')
            return redirect(url_for('add_item'))
        if not request.form['description']:
            flash('Please add a description')
            return redirect(url_for('add_item'))
        # If user is logged in, and all info provided, add item
        new_item = Items(name=request.form['name'],
                         description=request.form['description'],
                         category_id=request.form['category'],
                         user_id=login_session['user_id'])
        session.add(new_item)
        session.commit()
        # Return to homepage
        return redirect(url_for('home'))
    else:
        # Get all categories
        categories = session.query(Categories).all()
        # Render webpage
        return render_template('add_item.html', categories=categories)


@app.route('/<string:category>/<string:item>/edit',
           methods=['GET', 'POST'])
def edit_item(category, item):
    """App route function to edit an item."""
    # Verify user is logged in. If not, redirect to login page.
    if 'user_id' not in login_session:
        flash('Please log in.')
        return redirect(url_for('login'))
    # Get item to edit
    category = (session.query(Categories)
                .filter_by(name=category)
                .one())
    item = (session.query(Items)
            .filter_by(name=item.replace('-', ' '), category_id=category.id)
            .one())
    creator = (session.query(Users)
               .filter_by(id=item.creator_db_id)
               .one())
    # Only allow item creator to edit. If not, redirect to login.
    if creator.user_id != login_session['user_id']:
        return redirect(url_for('login'))
    # Get categories
    categories = session.query(Categories).all()
    # Show item to edit, or redirect
    if request.method == 'POST':
        if request.form['name']:
            Items.name = request.form['name']
        if request.form['description']:
            Items.description = request.form['description']
        if request.form['category']:
            Items.category_id = request.form['category']
        return redirect(url_for('show_item.html',
                                item=item,
                                category=category))
    else:
        # Render webpage
        return render_template('edit_item.html',
                               categories=categories,
                               item=item)


@app.route('/<string:category>/<string:item>/delete',
           methods=['GET', 'POST'])
def delete_item(category, item):
    """App route function to delete an item."""
    # Verify user is logged in. If not, redirect to login page.
    if 'user_id' not in login_session:
        flash('Please log in.')
        return redirect(url_for('login'))
    # Get item to edit
    category = (session.query(Categories)
                .filter_by(name=category)
                .one())
    item = (session.query(Items)
            .filter_by(name=item.replace('-', ' '), category_id=category.id)
            .one())
    creator = (session.query(Users)
               .filter_by(id=item.creator_db_id)
               .one())
    # Only allow item creator to edit. If not, redirect to login.
    if creator.user_id != login_session['user_id']:
        return redirect(url_for('login'))
    # Show item to delete, or redirect
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('home'))
    else:
        # Render webpage
        return render_template('delete_item.html', item=item)


"""
Logout
~~~~~~
"""


@app.route('/logout')
@app.route('/gdisconnect')
def gdisconnect():
    """App route function to disconnect from Google login."""
    try:
        access_token = login_session['credentials']
    except KeyError:
        flash('Failed to get access token')
        return redirect(url_for('home'))
    print('GDisconnect access token is {}'.format(access_token))
    print("User's name is {}".format(login_session['name']))
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    del login_session['credentials']
    del login_session['user_id']
    del login_session['name']
    del login_session['email']
    flash('Successfully logged out.')
    return redirect(url_for('home'))


# If this file is called as a standalone program:
if __name__ == '__main__':
    # Run the Flask app on port 8000 and enable debugging
    app.secret_key = CLIENT_SECRET
    app.run(host='0.0.0.0', port=8000, debug=True)
