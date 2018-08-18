"""
Udacity Full Stack Web Developer Nanodegree program (FSND)
Project 4. Flask Item Catalog App

application.py
~~~~~~~~~~~~~~

This file contains the main Flask application code.
"""

import json
import os
import random
import requests
import string

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
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True
    # Generate state token for Google Sign-In
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
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
                           login_status=login_status,
                           CLIENT_ID=CLIENT_ID,
                           STATE=state)


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
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True
    # Provide state token to enable Google Sign-In
    state = login_session['state']
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
                           login_status=login_status,
                           CLIENT_ID=CLIENT_ID,
                           STATE=state)


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
    # Detect login status
    login_status = None
    if 'email' in login_session:
        login_status = True
    # Provide state token to enable Google Sign-In
    state = login_session['state']
    # Query database with SQLAlchemy to show selected category and item
    category = (session.query(Categories)
                .filter_by(name=category.replace('-', ' '))
                .one())
    item = (session.query(Items)
            .filter_by(name=item.replace('-', ' '), category_id=category.id)
            .one())
    # Render webpage
    return render_template('show_item.html',
                           item=item,
                           category=category,
                           login_status=login_status,
                           CLIENT_ID=CLIENT_ID,
                           STATE=state)


@app.route('/<string:category>/<string:item>/json')
def show_item_json(category, item):
    """App route function to provide item data in JSON format."""
    category = (session.query(Categories)
                .filter_by(name=category.replace('-', ' '))
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
app.secret_key = CLIENT_SECRET


# Google Sign-In
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
    print('Result from Google access token is:', '\n', '{}.'
          .format(result))
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
            'User is already connected.'), 200)
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
    print('login_session object currently contains:', '\n', '{}'
          .format(login_session))
    # Check database for user
    user = (session.query(Users)
            .filter_by(email=login_session['email'])
            .first())
    if user:
        print('{} already exists.'.format(data['email']))
    # Create new user if user does not already exist
    else:
        new_user = Users(name=login_session['name'],
                         email=login_session['email'])
        session.add(new_user)
        session.commit()
        print('New user {} added to database.'.format(login_session['email']))
    output = ('<h3 class="font-weight-light">Welcome, {}!</h3>'
              .format(login_session['name']))
    flash('Logged in as {}.'.format(login_session['email']))
    print('Logged in as {}.'.format(login_session['email']))
    print('Done!')
    return output


# Standalone function in case user needs to be created without GConnect
def create_user(login_session):
    """Create new user based on login info."""
    new_user = Users(name=login_session['name'],
                     email=login_session['email'])
    session.add(new_user)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


"""
App route functions available after login
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    """App route function to create categories with POST requests."""
    # Verify user login. If not, redirect to login page.
    login_status = None
    if 'email' in login_session:
        login_status = True
    else:
        flash('Please log in.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Get form fields
        new_category_name = request.form['new_category_name']
        # Get user's database ID for the item's database entry
        user_db_id = (session.query(Users)
                      .filter_by(email=login_session['email'])
                      .one()).id
        print("Current user's database primary key id is {}."
              .format(user_db_id))
        # Flash messages for incomplete item info
        if not request.form['new_category_name']:
            flash('Please add category name.')
            return redirect(url_for('add_category'))
            # Query database for item name
        category_name_in_db = (session.query(Categories.name)
                               .filter_by(name=new_category_name)
                               .all())
        # If the category name is already in the database, don't add
        if category_name_in_db:
            print('Category name "{}" already in database.'
                  .format(new_category_name))
            flash('Category name "{}" already in database.'
                  .format(new_category_name))
            return redirect(url_for('add_category'))
        # If user is logged in, and all info provided, add category
        new_category = Categories(
            name=new_category_name,
            creator_db_id=user_db_id)
        session.add(new_category)
        session.commit()
        print('Category {} successfully created.'.format(new_category_name))
        # Return to homepage
        return redirect(url_for('home'))
    else:
        # Render webpage
        return render_template('add_category.html',
                               login_status=login_status)


@app.route('/<string:category>/edit', methods=['GET', 'POST'])
def edit_category(category):
    """App route function to edit categories."""
    # Verify user login. If not, redirect to login page.
    login_status = None
    if 'email' in login_session:
        login_status = True
    else:
        flash('Please log in.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Query database with SQLAlchemy and store query as an object
        category = (session.query(Categories)
                    .filter_by(name=category.replace('-', ' '))
                    .one())
        # Get form fields
        edit_category_name = request.form['edit_category_name']
        # Get user's database ID
        user_db_id = (session.query(Users)
                      .filter_by(email=login_session['email'])
                      .one()).id
        # Get database ID of category creator
        creator_db_id = category.creator_db_id
        print("Current user's database primary key id is {}."
              .format(user_db_id))
        print("Category creator's database primary key id is {}."
              .format(creator_db_id))
        print('Category to edit is "{}".'.format(category.name))
        # Only allow creator to edit. If not, redirect to login.
        if user_db_id != creator_db_id:
            flash('Only the creator can edit. Please log in as creator.')
            return redirect(url_for('home'))
        # Flash messages for incomplete item info
        if not request.form['edit_category_name']:
            flash('Please identify category.')
            return redirect(url_for('edit_category'))
        # Overwrite object with new info for database
        category.name = edit_category_name
        print('Category name for database is "{}".'.format(category.name))
        session.add(category)
        session.commit()
        # Return to homepage
        return redirect(url_for('home'))
    else:
        # Render webpage
        return render_template('edit_category.html',
                               category_name=category,
                               login_status=login_status)


@app.route('/<string:category>/delete', methods=['GET', 'POST'])
def delete_category(category):
    """App route function to delete categories."""
    # Verify user login. If not, redirect to login page.
    login_status = None
    if 'email' in login_session:
        login_status = True
    else:
        flash('Please log in.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Query database with SQLAlchemy and store queries as objects
        category = (session.query(Categories)
                    .filter_by(name=category.replace('-', ' '))
                    .one())
        category_items = (session.query(Items)
                          .filter_by(category_id=category.id)
                          .order_by(Items.name)
                          .all())
        # Get user's database ID
        user_db_id = (session.query(Users)
                      .filter_by(email=login_session['email'])
                      .one()).id
        # Get database ID of category creator
        creator_db_id = category.creator_db_id
        print("Current user's database primary key id is {}."
              .format(user_db_id))
        print("Category creator's database primary key id is {}."
              .format(creator_db_id))
        print('Category to delete is "{}".'.format(category.name))
        print('Items to delete:')
        for item in category_items:
            print(item.name)
        # Only allow creator to edit. If not, redirect to login.
        if user_db_id != creator_db_id:
            flash('Only the creator can edit. Please log in as creator.')
            return redirect(url_for('home'))
        session.delete(category)
        for item in category_items:
            session.delete(item)
        session.commit()
        # Return to homepage
        return redirect(url_for('home'))
    else:
        # Render webpage
        return render_template('delete_category.html',
                               category_name=category,
                               login_status=login_status)


@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    """App route function to create items with POST requests."""
    # Verify user login. If not, redirect to login page.
    login_status = None
    if 'email' in login_session:
        login_status = True
    else:
        flash('Please log in.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Get form fields
        name = request.form['name']
        url = request.form['url']
        photo_url = request.form['photo_url']
        description = request.form['description']
        category = request.form['item_category']
        # Retrieve the database ID of the selected category
        category_id = (session.query(Categories)
                       .filter_by(name=category.replace('-', ' '))
                       .one())
        # Retrieve user's database ID for the item's database entry
        user_db_id = (session.query(Users)
                      .filter_by(email=login_session['email'])
                      .one()).id
        print("Current user's database primary key id is {}."
              .format(user_db_id))
        print('Database ID of category is {}.'.format(category_id.id))
        # Flash messages for incomplete item info
        if not request.form['name']:
            flash('Please add item name')
            return redirect(url_for('add_item'))
        if not request.form['url']:
            flash('Please add item URL')
            return redirect(url_for('add_item'))
        if not request.form['photo_url']:
            flash('Please add item photo URL')
            return redirect(url_for('add_item'))
        if not request.form['description']:
            flash('Please add a description')
            return redirect(url_for('add_item'))
        # Query database for item name
        item_name_in_db = (session.query(Items.name)
                           .filter_by(name=name)
                           .all())
        # If the item name is already in the database, don't add
        if item_name_in_db:
            print('Item name "{}" already in database.'.format(name))
            flash('Item name "{}" already in database.'.format(name))
            return redirect(url_for('add_item'))
        # Create object with form field info to add to database
        new_item = Items(name=name,
                         url=url,
                         photo_url=photo_url,
                         description=description,
                         category_id=category_id.id,
                         creator_db_id=user_db_id)
        session.add(new_item)
        session.commit()
        print('Item "{}" created.'.format(new_item.name))
        # Return to homepage
        return redirect(url_for('home'))
    else:
        # Query database with SQLAlchemy to display categories on page
        categories = session.query(Categories).all()
        # Render webpage
        return render_template('add_item.html',
                               categories=categories,
                               login_status=login_status)


@app.route('/<string:category>/<string:item>/edit',
           methods=['GET', 'POST'])
def edit_item(category, item):
    """App route function to edit an item."""
    # Verify user login. If not, redirect to login page.
    login_status = None
    if 'email' in login_session:
        login_status = True
    else:
        flash('Please log in.')
        return redirect(url_for('home'))
    # Query database with SQLAlchemy to display categories on page
    categories = session.query(Categories).all()
    if request.method == 'POST':
        # Query database with SQLAlchemy and store queries as objects
        category = (session.query(Categories)
                    .filter_by(name=category.replace('-', ' '))
                    .one())
        item = (session.query(Items)
                .filter_by(name=item.replace('-', ' '))
                .one())
        # Get form fields submitted by user, or retain item info
        if request.form['name']:
            name = request.form['name']
        else:
            name = item.name
        if request.form['url']:
            url = request.form['url']
        else:
            url = item.url
        if request.form['photo_url']:
            photo_url = request.form['photo_url']
        else:
            photo_url = item.photo_url
        if request.form['description']:
            description = request.form['description']
        else:
            description = item.description
        category = request.form['item_category']
        # Retrieve the database ID of the item's category
        category_id = (session.query(Categories)
                       .filter_by(name=category.replace('-', ' '))
                       .one())
        # Get user's database ID
        user_db_id = (session.query(Users)
                      .filter_by(email=login_session['email'])
                      .one()).id
        # Get database ID of creator
        creator_db_id = item.creator_db_id
        print("Current user's database primary key id is {}."
              .format(user_db_id))
        print("Item creator's database primary key id is {}."
              .format(creator_db_id))
        print('Item to edit is "{}".'.format(item.name))
        # Only allow creator to edit. If not, redirect to login.
        if user_db_id != creator_db_id:
            flash('Only the creator can edit. Please log in as creator.')
            return redirect(url_for('home'))
        # Store edits in an object
        edited_item = Items(name=name,
                            url=url,
                            photo_url=photo_url,
                            description=description,
                            category_id=category_id.id,
                            creator_db_id=user_db_id)
        # Overwrite item object with new info from edited_item object
        item.name = edited_item.name
        item.url = edited_item.url
        item.photo_url = edited_item.photo_url
        item.description = edited_item.description
        item.category_id = edited_item.category_id
        session.add(item)
        session.commit()
        print('Item "{}" edited.'.format(edited_item.name))
        # Return to homepage
        return redirect(url_for('home'))
    else:
        # Query database with SQLAlchemy to display categories on page
        categories = session.query(Categories).all()
        # Render webpage
        return render_template('edit_item.html',
                               categories=categories,
                               item=item,
                               login_status=login_status)


@app.route('/<string:category>/<string:item>/delete',
           methods=['GET', 'POST'])
def delete_item(category, item):
    """App route function to delete an item."""
    # Verify user login. If not, redirect to login page.
    login_status = None
    if 'email' in login_session:
        login_status = True
    else:
        flash('Please log in.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Query database with SQLAlchemy and store queries as objects
        category = (session.query(Categories)
                    .filter_by(name=category.replace('-', ' '))
                    .one())
        item = (session.query(Items)
                .filter_by(name=item
                           .replace('-', ' '), category_id=category.id)
                .one())
        # Get user's database ID
        user_db_id = (session.query(Users)
                      .filter_by(email=login_session['email'])
                      .one()).id
        # Get database ID of creator
        creator_db_id = item.creator_db_id
        print("Current user's database primary key id is {}."
              .format(user_db_id))
        print("Item creator's database primary key id is {}."
              .format(creator_db_id))
        print('Item to delete is "{}".'.format(item.name))
        # Only allow creator to edit. If not, redirect to login.
        if user_db_id != creator_db_id:
            flash('Only the creator can edit. Please log in as creator.')
            return redirect(url_for('home'))
        session.delete(item)
        session.commit()
        # Return to homepage
        return redirect(url_for('home'))
    else:
        # Render webpage
        return render_template('delete_item.html',
                               item=item,
                               login_status=login_status)


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
    print("User's name was {}.".format(login_session['name']))
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
    print('Successfully logged out.')
    flash('Successfully logged out.')
    return redirect(url_for('home'))


# If this file is called as a standalone program:
if __name__ == '__main__':
    app.run(
        host=os.environ.get('APP_HOST') or '0.0.0.0',
        port=os.environ.get('APP_PORT') or 5000
    )
