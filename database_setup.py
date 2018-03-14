#!/usr/bin/env python3

# Udacity Full Stack Web Developer Nanodegree program (FSND)
# Part 03. Backend
# Project 02. Flask Item Catalog App

# Import SQLAlchemy modules for database
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask import jsonify
import datetime

Base = declarative_base()


# Use Python classes to establish database tables
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


class CatalogItem(Base):
    """Create a database table for items."""
    __tablename__ = 'catalog_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


# TODO: why is it sqlite here
engine = create_engine('sqlite:///restaurantmenu.db')


Base.metadata.create_all(engine)
