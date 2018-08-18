"""
Udacity Full Stack Web Developer Nanodegree program (FSND)
Project 4. Flask Item Catalog App

database_data.py
~~~~~~~~~~~~~~~~

This file contains information used to populate the Flask app database.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categories, Items, Users


"""
Connect to database and establish database session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# Configure SQLAlchemy engine
engine = create_engine('sqlite:///catalog.db')

# Bind engine to metadata of Base class
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


"""
Populate database
~~~~~~~~~~~~~~~~~
"""

# User
if os.environ.get('USER_NAME') and os.environ.get('USER_EMAIL'):
    user_name = os.environ.get('USER_NAME')
    user_email = os.environ.get('USER_EMAIL')
else:
    # Request input from user
    print('\n', 'Provide credentials to be used when populating the database')
    user_name = input('Please enter your name: ')
    user_email = input('Please enter your email address: ')
# Query database for user email
user_email_in_db = (session.query(Users.email)
                    .filter_by(email=user_email)
                    .all())
if user_email_in_db:
    print('User {} already in database.'.format(user_email))
    user = Users(name=user_name, email=user_email)
else:
    # Create new user
    new_user = Users(name=user_name, email=user_email)
    session.add(new_user)
    session.commit()
    print('User {} successfully added to database.'.format(new_user.email))
    user = new_user


# Categories
def check_db_for_category(category):
    """Helper function to check database for category before adding."""
    # Query database for category
    category_in_db = (session.query(Categories.name)
                      .filter_by(name=category.name)
                      .all())
    # If the category name is already present in the database, don't add it
    if category_in_db:
        print('Category "{}" already in database.'.format(category.name))
    # Else, add category to database
    else:
        session.add(category)
        session.commit()
        print('Category "{}" added to database.'.format(category.name))


category = Categories(name='Equipment', user=user)
check_db_for_category(category)
# Create object for database category so items below can be added
equipment = session.query(Categories).filter_by(name='Equipment').one()

category = Categories(name='Accessories', user=user)
check_db_for_category(category)
# Create object for database category so items below can be added
accessories = session.query(Categories).filter_by(name='Accessories').one()


# Items
def check_db_for_item(item):
    """Helper function to check database for item before adding."""
    # Check database for item
    item_in_db = (session.query(Items.name)
                  .filter_by(name=item.name)
                  .all())
    # If the item name is already present in the database, don't add it
    if item_in_db:
        print('Item "{}" already in database.'.format(item.name))
    # Else, add item to database
    else:
        session.add(item)
        session.commit()
        print('Item "{}" added to database.'.format(item.name))


item = Items(name='Hoist Dual Action Leg Press',
             url=('https://www.hoistfitness.com/commercial/equipment/'
                  'rpl-5403_dual-action-leg-press'),
             photo_url=('https://www.hoistfitness.com/content/images/'
                        'equipment/360view/RPL-5403/000007.jpg'),
             description=('This Hoist composite motion leg press is, by far,'
                          ' the best leg press I have used. The arc motion'
                          ' activates the posterior chain and protects the'
                          ' knees. Build your legs on this beast!'),
             category=equipment,
             user=user)
check_db_for_item(item)

item = Items(name='Hoist Power Cage',
             url=('https://www.hoistfitness.com/commercial/equipment/'
                  'cf-3364_power-cage'),
             photo_url=('https://www.hoistfitness.com/content/images/'
                        'equipment/CF-3364.JPG?width=348'),
             description=('Gotta have a power cage. This one features'
                          ' top-quality Hoist construction,'
                          ' easy adjustments, and a pull-up bar.'),
             category=equipment,
             user=user)
check_db_for_item(item)

item = Items(name='Pro Monster Mini Resistance Band',
             url=('http://a.co/3sUV4b2'),
             photo_url=('https://images-na.ssl-images-amazon.com/images/I/'
                        '31TEsfuiulL._SX425_.jpg'),
             description=('Add dynamic resistance to exercises'
                          ' with these super strong bands.'),
             category=accessories,
             user=user)
check_db_for_item(item)

item = Items(name='Fat Gripz',
             url=('http://www.fatgripz.com/'),
             photo_url=('http://www.fatgripz.com/images/columns-8.jpg'),
             description=('Stick these on any bar or handle to'
                          ' build up your grip strength.'),
             category=accessories,
             user=user)
check_db_for_item(item)

item = Items(name='RumbleRoller',
             url=('https://www.rumbleroller.com/'),
             photo_url=('https://www.rumbleroller.com/rr2-images/godeeper-'
                        '1920x390.jpg'),
             description=('This roller will change your life.'
                          ' Release soft tissue and roll out knots.'),
             category=accessories,
             user=user)
check_db_for_item(item)

item = Items(name='SlingShot Hip Circle 2.0',
             url=('https://markbellslingshot.com/collections/'
                  'hip-circles/products/hip-circle-2-0'),
             photo_url=('https://cdn.shopify.com/s/files/1/2233/5357/products'
                        '/20180207_Hip_Circle-1.jpg?v=1521136877'),
             description=('Wear this hip circle to activate leg, hip and'
                          ' lower back muscles. Great for leg workouts, or'
                          ' even standing computer work!'),
             category=accessories,
             user=user)
check_db_for_item(item)

print('Database population complete.', '\n')
