#!/usr/bin/env python3

# Udacity Full Stack Web Developer Nanodegree program (FSND)
# Part 03. Backend
# Project 02. Flask Item Catalog App
# Catalog of items

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
example_user = User(name='Bongo Strudel', email='big.bad.bongo@hotmail.com',
                    photo='https://picsum.photos/300/?random')

# Brendon's Bodybuilding Bazaar

# Category: Equipment
category_equipment = Category(name='Equipment')
session.add(category_equipment)
session.commit()

# Equipment items
leg_press = Item(name='Hoist Dual Action Leg Press',
                 description='This Hoist composite motion leg press is,'
                 ' by far, the best leg press machine I have used.'
                 ' The arc motion activates the posterior chain and'
                 ' protects the knees. Build your legs on this beast!',
                 category=category_equipment)
# url=('https://www.hoistfitness.com/commercial/equipment/'
# 'rpl-5403_dual-action-leg-press')
# img=('https://www.hoistfitness.com/commercial/equipment/'
# 'rpl-5403_dual-action-leg-press')
session.add(leg_press)
session.commit()

power_cage = Item(name='Hoist Power Cage',
                  description='Gotta have a power cage.'
                  ' This one features top-quality Hoist construction,'
                  'easy adjustments, and a pull-up bar.',
                  category=category_equipment)
# url='https://www.hoistfitness.com/commercial/equipment/cf-3364_power-cage'
# img='https://www.hoistfitness.com/content/images/equipment/'
# 'CF-3364.JPG?width=348'
session.add(power_cage)
session.commit()

# Category: Accessories
category_accessories = Category(name='Accessories')
session.add(category_accessories)
session.commit()

# Accessories items
band_monster_mini = Item(name='Pro Monster Mini Resistance Band',
                         description='Add dynamic resistance to your'
                         ' exercises with these super strong bands.',
                         category=category_accessories)
# url='https://www.elitefts.com/pro-monster-mini-restistance-band.html'
# img='https://www.elitefts.com/pro-monster-mini-restistance-band.html'
# Yes, they mis-spelled resistance in the url.
# They're good at strength training, not spelling.
session.add(band_monster_mini)
session.commit()

fat_gripz = Item(name='Fat Gripz',
                 description='Stick these on any bar or handle to'
                 ' build up your grip strength.',
                 category=category_accessories)
# url = 'http://www.fatgripz.com/'
# img = 'http://www.fatgripz.com/images/columns-8.jpg'
session.add(fat_gripz)
session.commit()

rumbleroller = Item(name='RumbleRoller',
                    description='This roller will change your life.'
                    'Release your soft tissue and roll out knots.',
                    category=category_accessories)
# url = 'https://www.rumbleroller.com/'
# img = 'https://www.rumbleroller.com/rr2-images/godeeper-1920x390.jpg'
session.add(rumbleroller)
session.commit()

slingshot_hip_2 = Item(name='SlingShot Hip Circle 2.0',
                       description='Wear this hip circle to activate'
                       ' leg, hip and lower back muscles. Great for'
                       ' leg workouts, or even standing computer work!',
                       category=category_accessories)
# url=('https://markbellslingshot.com/collections/hip-circles/products/'
# 'hip-circle-2-0')
# img=('https://cdn.shopify.com/s/files/1/2233/5357/products/'
# '20180207_Hip_Circle-1.jpg?v=1521136877')
session.add(slingshot_hip_2)
session.commit()

# Verify categories
categories = session.query(Category).all()
for category in categories:
    print('Category: {}'.format(category.name))
