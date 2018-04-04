#!/usr/bin/env python3

"""
Udacity Full Stack Web Developer Nanodegree program (FSND)
Project 4. Flask Item Catalog App

catalog.py
~~~~~~~~~~

This file contains information used to populate the Flask app database.
"""

# Import SQLAlchemy modules for database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# Configure SQLAlchemy engine
engine = create_engine('sqlite:///catalog.db')
# Bind engine to metadata of Base class
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create example user
example_user = User(name='Bongo Strudel',
                    email='big.bad.bongo@hotmail.com',
                    photo='https://picsum.photos/300/?random')
session.add(example_user)
session.commit()

# Brendon's Bodybuilding Bazaar

# Category: Equipment
category_equipment = Category(name='Equipment', user=example_user)
session.add(category_equipment)
session.commit()

# Category: Accessories
category_accessories = Category(name='Accessories', user=example_user)
session.add(category_accessories)
session.commit()

# Equipment items
leg_press = Item(name='Hoist Dual Action Leg Press',
                 url=('https://www.hoistfitness.com/commercial/equipment/'
                      'rpl-5403_dual-action-leg-press'),
                 photo=('https://www.hoistfitness.com/content/images/'
                        'equipment/360view/RPL-5403/000007.jpg'),
                 description=('This Hoist composite motion leg press is,'
                              ' by far, the best leg press I have used.'
                              ' The arc motion activates the posterior chain'
                              ' and protects the knees. Build your legs on'
                              ' this beast!'),
                 category=category_equipment,
                 user=example_user)
session.add(leg_press)
session.commit()

power_cage = Item(name='Hoist Power Cage',
                  url=('https://www.hoistfitness.com/commercial/equipment/'
                       'cf-3364_power-cage'),
                  photo=('https://www.hoistfitness.com/content/images/'
                         'equipment/CF-3364.JPG?width=348'),
                  description=('Gotta have a power cage. This one features'
                               ' top-quality Hoist construction,'
                               'easy adjustments, and a pull-up bar.'),
                  category=category_equipment,
                  user=example_user)
session.add(power_cage)
session.commit()


# Accessories items
band_monster_mini = Item(name='Pro Monster Mini Resistance Band',
                         url=('http://a.co/3sUV4b2'),
                         photo=('https://images-na.ssl-images-amazon.com/'
                                'images/I/31TEsfuiulL._SX425_.jpg'),
                         description=('Add dynamic resistance to exercises'
                                      ' with these super strong bands.'),
                         category=category_accessories,
                         user=example_user)
session.add(band_monster_mini)
session.commit()

fat_gripz = Item(name='Fat Gripz',
                 url=('http://www.fatgripz.com/'),
                 photo=('http://www.fatgripz.com/images/columns-8.jpg'),
                 description=('Stick these on any bar or handle to'
                              ' build up your grip strength.'),
                 category=category_accessories,
                 user=example_user)
session.add(fat_gripz)
session.commit()

rumbleroller = Item(name='RumbleRoller',
                    url=('https://www.rumbleroller.com/'),
                    photo=('https://www.rumbleroller.com/rr2-images/'
                           'godeeper-1920x390.jpg'),
                    description=('This roller will change your life.'
                                 'Release soft tissue and roll out knots.'),
                    category=category_accessories,
                    user=example_user)

session.add(rumbleroller)
session.commit()

slingshot_hip_2 = Item(name='SlingShot Hip Circle 2.0',
                       url=('https://markbellslingshot.com/collections/'
                            'hip-circles/products/hip-circle-2-0'),
                       photo=('https://cdn.shopify.com/s/files/1/2233/5357/'
                              'products/20180207_Hip_Circle-1.jpg'
                              '?v=1521136877'),
                       description=('Wear this hip circle to activate'
                                    ' leg, hip and lower back muscles.'
                                    ' Great for leg workouts, or even'
                                    ' standing computer work!'),
                       category=category_accessories,
                       user=example_user)

session.add(slingshot_hip_2)
session.commit()

# Verify categories
categories = session.query(Category).all()
for category in categories:
    print('Category: {}'.format(category.name))
