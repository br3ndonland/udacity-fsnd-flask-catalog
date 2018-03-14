#!/usr/bin/env python3

# Udacity Full Stack Web Developer Nanodegree program (FSND)
# Part 03. Backend
# Project 02. Flask Item Catalog App

# Import SQLAlchemy modules for database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem

# Import Flask class from flask library
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Create an instance of class Flask
# Each time the application runs, a special variable 'name' is defined.
app = Flask(__name__)


# Decorators to wrap each function inside Flask's app.route() function

# Homepage
@app.route('/')
def hello_world():
    """App route function for the homepage."""
    return 'Hello World!'


# GET request
@app.route('/readHello')
def get_request_hello():
    """Function that defines app response to GET requests."""
    return "Hi, I got your GET Request!"


# POST request
@app.route('/createHello', methods=['POST'])
def post_request_hello():
    """Function that defines app response to POST requests."""
    return "I see you sent a POST message :-)"


# UPDATE request
@app.route('/updateHello', methods=['PUT'])
def update_request_hello():
    """Function that defines app response to PUT requests."""
    return "Sending Hello on an PUT request!"


# DELETE request
@app.route('/deleteHello', methods=['DELETE'])
def delete_request_hello():
    """Function that defines app response to DELETE requests."""
    return "Received a DELETE request!"


# If this file is called as a standalone program:
if __name__ == '__main__':
    # Run the Flask app on port 8000 and enable debugging
    app.run(host='0.0.0.0', port=8000, debug=True)
