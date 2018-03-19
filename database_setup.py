#!/usr/bin/env python3

# Udacity Full Stack Web Developer Nanodegree program (FSND)
# Part 03. Backend
# Project 02. Flask Item Catalog App
# Database setup code

# Import SQLAlchemy modules for database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

# Use Python classes to establish database tables


class User(Base):
    """Create a database table for application users."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    photo = Column(String(250))


class Category(Base):
    """Create a database table for item categories."""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    """Create a database table for items."""
    __tablename__ = 'catalog_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category.name,
            'id': self.id,
        }


# Configure SQLAlchemy engine
engine = create_engine('sqlite:///catalog.db')
# Create database
Base.metadata.create_all(engine)
