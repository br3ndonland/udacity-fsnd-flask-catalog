# Project methods

<a href="https://www.udacity.com/">
    <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
</a>

**Udacity Full Stack Web Developer Nanodegree program**

Part 03. Backend

[Project 02. Flask Item Catalog App](https://github.com/br3ndonland/udacity-fsnd03-p02-flask-catalog)

Brendon Smith

br3ndonland

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Environment and documentation setup](#environment-and-documentation-setup)
- [Directory setup](#directory-setup)
- [Database setup](#database-setup)
- [Application setup](#application-setup)
- [Step 3: Installing app as a package](#step-3-installing-app-as-a-package)
- [Step 4: Database connections](#step-4-database-connections)
- [Step 5: Creating the database](#step-5-creating-the-database)
- [Step 6: The view functions](#step-6-the-view-functions)
- [Step 7: The templates](#step-7-the-templates)
- [Step 8: Adding style](#step-8-adding-style)
- [Testing the application](#testing-the-application)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Environment and documentation setup
[(back to top)](#top)

### Virtual machine

I already had the vagrant virtual machine environment installed and ready to go.


### Docs

* I created the basic outline of the [README](README.md).
* I read through the Udacity documentation and rubric, and added the materials to the repo in [flask-catalog-udacity-docs.md](flask-catalog-udacity-docs.md).
	- The documentation is open-ended on how to work through construction of the app.
		> Whether you start on the front end or the back end is up to you. Some people prefer seeing the layout before thinking about the data they want to present, whereas others enjoy thinking about the structure and organization of their data and the Flask application before beginning on the front end portion of their project.
	- Instructor Lorenzo Brown seems to prefer a back-end-first approach:
		> Personally, I usually start with the database layout so that the database is modelling the information the way I want. Then I go ahead and add the backend, the Flask code, the Python code, and then I move on to the frontend where I then receive feedback on the frontend where I use the feedback to make it more stylish and elegant and presentable with everything else already in place. This is just me though, it varies from developer to developer.
		
		Not that helpful, or even grammatical.
	- Lorenzo's lesson on agile iterative development (Full Stack Foundations Lesson 4, FSND Part 03 Lesson 09) actually walks through a front-end-first approach, starting with mockups.
* I reviewed my course notes, and walked through [my notes on the Flask lesson](https://github.com/br3ndonland/udacity-fsnd/blob/master/03-backend/06-09-foundations/fsnd03_08-flask.md), and the [Flask app code from the lesson](https://github.com/udacity/Full-Stack-Foundations) in Full-Stack-Foundations/Lesson-3/Final-Flask-Application.
* The **[Flask tutorial](http://flask.pocoo.org/docs/0.12/tutorial/)** gave me a helpful step-by-step outline of the app creation process.
* **I compared the steps from the Udacity lesson and the Flask tutorial to make my own app.**


## Directory setup
[(back to top)](#top)

* I created a directory at */vagrant/flask-catalog* for the application, and set up the basic structure of the app directory.
* The **[Flask docs](http://flask.pocoo.org/docs/0.12/)** had some helpful instructions in the foreword for how to organize the directory:
	> [Configuration and Conventions](http://flask.pocoo.org/docs/0.12/foreword/#configuration-and-conventions)
	> 
	> Flask has many configuration values, with sensible defaults, and a few conventions when getting started. By convention, templates and static files are stored in subdirectories within the application’s Python source tree, with the names templates and static respectively. While this can be changed, you usually don’t have to, especially when getting started.
* I also referred to the **[Flask tutorial](http://flask.pocoo.org/docs/0.12/tutorial/)**:
	> [Step 0: Creating The Folders](http://flask.pocoo.org/docs/0.12/tutorial/folders/)
	> 
	> Before getting started, you will need to create the folders needed for this application:
	> ```
	> /flaskr
	>   /flaskr
	>     /static
	>     /templates
	> ```
	**I elected not to create two top-level folders.**
* I created [application.py](application.py) for the main Flask application.
* I added the */static* directory for CSS and JavaScript.
* I added the */templates* directory for the HTML webpages.


## Database setup
[(back to top)](#top)

### database_setup.py

#### SQLAlchemy imports

As we did in lesson 6, I will perform CRUD operations with SQLAlchemy on an SQLite database. The SQL database is established within *database_setup.py*. I also read through the SQLite instructions in the [Flask tutorial](http://flask.pocoo.org/docs/0.12/tutorial/schema/), but I may not need the *schema.sql file*.

We first import the necessary modules:

## Step 2: Application setup code
[(back to top)](#top)

* I adapted the [api_server.py](https://github.com/udacity/APIs/blob/master/Lesson_2/06_Sending%20API%20Requests/api_server.py) from 15.05 (APIs course, lesson 2) to set up the basic app at [application.py](application.py).

## Step 3: Installing app as a package
[(back to top)](#top)

## Step 4: Database connections
[(back to top)](#top)

## Step 5: Creating the database
[(back to top)](#top)

TODO: KONRAD JUST HARDCODED THE ITEMS INTO INIT_DB_SETUP.PY

## Step 6: The view functions
[(back to top)](#top)

### Show entries
### Add new entry

### Authentication: Login and Logout

### CSRF protection

Cross-Site Request Forgery (CSRF)

[CSRF protection in Flask](http://flask.pocoo.org/snippets/3/)


## Step 7: The templates
[(back to top)](#top)


* layout.html
* show_entries.html
* login.html

## Step 8: Adding style
[(back to top)](#top)

### HTML and CSS

TODO: IMPORT BOOTSTRAP


## Testing the application
[(back to top)](#top)

### API endpoints


[(back to top)](#top)