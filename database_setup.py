"""
Udacity Full Stack Web Developer Nanodegree program (FSND)
Project 4. Flask Item Catalog App

database_setup.py
~~~~~~~~~~~~~~~~~

This file sets up the SQL database for the Flask app.
"""

# Import SQLAlchemy modules for database
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


# Use Python classes to establish database tables
class Users(Base):
    """Create a database table for application users."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Categories(Base):
    """Create a database table for item categories."""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    creator_db_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Items(Base):
    """Create a database table for items."""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    url = Column(String(250))
    photo_url = Column(String(250))
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship(Categories)
    date_created = Column(DateTime, default=datetime.datetime.now())
    creator_db_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category.name,
            'date created': self.date_created,
            'id': self.id
        }


# Configure SQLAlchemy engine
engine = create_engine('sqlite:///catalog.db')

# Create database
Base.metadata.create_all(engine)

if __name__ == '__main__':
    # Print results to the command line
    print('Database created.', '\n')
