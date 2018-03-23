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
- [Application](#application)
- [Authentication and authorization](#authentication-and-authorization)
- [Templates](#templates)
- [Style](#style)
- [Testing](#testing)

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

As we did in lesson 6, I will perform CRUD operations with SQLAlchemy on an SQLite database. The SQL database is established within [database_setup.py](database_setup.py). I also read through the SQLite instructions in the [Flask tutorial](http://flask.pocoo.org/docs/0.12/tutorial/schema/), but I may not need the schema.sql file.

We first import the necessary modules:

```python
# Import SQLAlchemy modules for database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem, User
```


#### Classes

Next, I needed to create Python classes for the different tables in the database. We need a database of items in different categories for this project. This is similar to having restaurants with different menu items in the Udacity lesson. I was therefore able to easily adapt the `class Restaurant(Base)` to `class Category(Base)`, and `class MenuItem(Base)` to class `CatalogItem(Base)`. I added a `class User(Base)` to keep track of users registered for the app.


#### SQLAlchemy engine and database creation

Next, we need to [configure the SQLAlchemy engine](http://docs.sqlalchemy.org/en/latest/core/engines.html):

```python
engine = create_engine('sqlite:///restaurantmenu.db')
```

The [SQLAlchemy SQLite](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlite) URL has three slashes for a relative file path.

Finally, we use SQLAlchemy to create the SQLite database:

```python
Base.metadata.create_all(engine)
```


### catalog.py

#### Setup

Now that I have database_setup.py to set up my database, I need to populate the database with items for the catalog. I based [catalog.py](catalog.py) on [lotsofmenus.py](https://github.com/udacity/Full-Stack-Foundations/blob/master/Lesson-4/Final-Project/lotsofmenus.py) from the Full Stack Foundations course.

As with database_setup.py, I started off adding in the necessary SQLAlchemy imports and configuring the SQLAlchemy engine.

Next, we need to:

> Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance

```python
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
```

After we bind the engine to the Base class, we need to establish a database session. The comments in lotsofmenus.py explain:

> A `DBSession()` instance establishes all conversations with the database and represents a "staging zone" for all the objects loaded into the database session object. Any change made against the objects in the session won't be persisted into the database until you call `session.commit()`. If you're not happy about the changes, you can revert all of them back to the last commit by calling `session.rollback()`.


#### Categories and items

Now that catalog.py is set up, I will start adding items. I used a film noir theme for my [movie trailer site](https://github.com/br3ndonland/udacity-fsnd01-p01-movies), so here I will bring in another one of my interests: Bodybuilding! Welcome to Brendon's Bodybuilding Bazaar! I entered some brief info about some of my favorite strength training equipment and accessories.

I knew from experience that Python concatenates adjacent strings, so I broke the descriptions into multiple strings, with one string per line.

I included website and image URLs, and commented them out, in case I want to use them in the future.


### Database creation

When I first tried to create the database with

```bash
$ python3 database_setup.py
```

I was getting errors because of the `datetime` code.

```
Traceback (most recent call last):
  File "database_setup.py", line 45, in <module>
    class Item(Base):
  File "database_setup.py", line 54, in Item
    date_created = Column(datetime, default=datetime.datetime.now())
  File "/usr/local/lib/python3.5/dist-packages/sqlalchemy/sql/schema.py", line 1279, in __init__
    self._init_items(*args)
  File "/usr/local/lib/python3.5/dist-packages/sqlalchemy/sql/schema.py", line 90, in _init_items
    item._set_parent_with_dispatch(self)
AttributeError: module 'datetime' has no attribute '_set_parent_with_dispatch'
```

I included a `date_created` object for each of the items, so the most recent items can be shown on the homepage.

I moved to the command line to troubleshoot this. My first progress came when changing `import datetime` to `from datetime import datetime`. Confusing nomenclature.

```
>>> from datetime import datetime
>>> print(datetime.now())
2018-03-22 22:12:03.950458
```

Now I need to adjust the timezone to local time. It looks like Python doesn't have built-in support for time zones.

I put this code back into database_setup.py, but was still getting the same error.

I realized that I should probably use SQLAlchemy to calculate the time.

I changed the code for SQLAlchemy:

```python
date_created = Column(datetime(timezone=True), default=func.now())
```

Which then threw another error:

```
vagrant@vagrant:/vagrant/flask-catalog$ python3 database_setup.py
Traceback (most recent call last):
  File "database_setup.py", line 45, in <module>
    class Item(Base):
  File "database_setup.py", line 54, in Item
    date_created = Column(datetime(timezone=True), default=func.now())
TypeError: Required argument 'year' (pos 1) not found
```

I tried it several more times, and finally got it to work. **The solution was to have two datetime imports, from Python and Flask.** Confusing.

Here are the imports I needed in database_setup.py for the datetime to work:

```python
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
```

Here is the code I needed to timestamp item creation:

```python
class Item(Base):
    """Create a database table for items."""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    date_created = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

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


```

Git commit at this point: Debug database item timestamping 695e7bb


### Database population

I populated the database with items from catalog.py by running:

```
vagrant@vagrant:/vagrant/flask-catalog$ python3 catalog.py
Category: Equipment
Category: Accessories
```

I verified the additions to the database using [DB Browser for SQLite](http://sqlitebrowser.org/):

<img src="img/database-population.png" alt="Screenshot of DB Browser for SQLite, showing successful database creation and population" width="75%">


## Application
[(back to top)](#top)

Now that I have the database and catalog set up, it's time to code the main application in [application.py](application.py). If you're still following along in the [Flask tutorial](http://flask.pocoo.org/docs/0.12/tutorial/), this would roughly be around [Step 6: The view functions](http://flask.pocoo.org/docs/0.12/tutorial/views/).


### application.py

#### Setup

* I started with the usual imports and database connection.
* Before any operations are performed, we must first import the necessary libraries, connect to the database, and create a session to interface with the database. SQLAlchemy uses "sessions" to connect to the database. We can store the commands we plan to use, but not send them to the database until we run a commit.


#### App routes

* **The lessons didn't adequately prepare me for building the rest of the application code.** I started, as before, by reviewing code from the Full Stack Foundations restaurant menus example. I referenced [finalproject.py](https://github.com/udacity/Full-Stack-Foundations/blob/master/Lesson-4/Final-Project/finalproject.py).
* **I decided to start by defining functions for the Flask app routes, and then to leave the authentication flow for later.**


##### CRUD: Read

* The homepage app route was fairly straightforward. The most difficult thing was figuring out how to display recent items. I accomplished this by creating a `recent_items` object and using a [SQLAlchemy command](https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending#4187279):
	```python
	    recent_items = (session.query(Item)
        .order_by(Item.date_created.desc())
        .limit(10)
        .all())
	```
* Next, I coded the app route function to display all items in a specific category. The URL in [finalproject.py](https://github.com/udacity/Full-Stack-Foundations/blob/master/Lesson-4/Final-Project/finalproject.py) is coded using the category `id`, which is okay, but it may be more intuitive to use the category name in the URL.
<!-- TODO: Re-code URL with category name -->


##### CRUD: Create an item with a POST request

* The next function to build in would be item creation. We will use POST requests for this.
* Users need to be logged in to edit items. I added a simple login verification:
	```python
	# Verify user is logged in
	if 'username' not in login_session:
	    return redirect('/login')
	```
* I will build in additional login functions later.
* Next, I needed flash messages to warn users if they haven't added all the information needed for a new item. I used the Flask lesson from Full Stack Foundations, Part 15, as a starting point (see [lesson notes](https://github.com/br3ndonland/udacity-fsnd/blob/master/04-web-apps/06-09-foundations/fsnd03_08-flask.md#message-flashing) and [lesson code](https://github.com/br3ndonland/Full-Stack-Foundations/blob/master/Lesson-3/17_Flash-Messaging-Solution/project.py))
* I added in the `from Flask import flash` to support flash messaging.
* I then added an object to provide all the proper fields for the item, based on database_setup.py.


##### CRUD: Edit and delete items

* Of course, after we create items, we may want to edit or delete them.
* We only want the creator of the item to be able to modify it.


##### JSON

I created additional app routes with `jsonify` by appending '/json' to the homepage, category, and item pages.

For example:

```python
@app.route('/catalog/<int:category_id>/json`')
@app.route('/catalog/<int:category_id>/items/json')
def show_category_json(category_id):
    """App route function to provide category data in JSON format."""
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[items.serialize for item in items])
```


### Next steps

I did a Git commit at this point (Create app routes, 0bcddf7), and thought about how to proceed. I could have built the HTML templates and tested the app, but decided to proceed with authentication and build the front-end later.


## Authentication and authorization

### Getting started

I turned to [my notes](https://github.com/br3ndonland/udacity-fsnd/blob/master/04-web-apps/10-13-oauth/fsnd03_10-13-oauth.md) and the [material](https://github.com/udacity/OAuth2.0) from the [OAuth lessons](https://www.udacity.com/course/authentication-authorization-oauth--ud330) to implement Google and Facebook sign-in.

The Udacity materials are, of course, poorly formatted and outdated, and didn't prepare me for the project.

The instructor notes in Lesson 10.02 Authentication and Authorization link to [lepture's blog post about Flask-OAuthlib](http://lepture.com/en/2013/create-oauth-server). He was the creator of Flask-OAuthlib and has now replaced it with the [announcement of Authlib](https://lepture.com/en/2018/announcement-of-authlib).

How does this relate to Google and Facebook sign-in, and do I need it?


### Google

### Facebook

### CSRF protection

Cross-Site Request Forgery (CSRF)

[CSRF protection in Flask](http://flask.pocoo.org/snippets/3/)


## Templates
[(back to top)](#top)

flask tutorial step 7

* I started by quickly creating the files I knew I needed on the command line:
	```bash
	touch index.html categories.html category.html item.html add_item.html edit_item.html delete_item.html login.html
	```
* 

## Style
[(back to top)](#top)

### HTML and CSS

TODO: IMPORT BOOTSTRAP


## Testing
[(back to top)](#top)


[(back to top)](#top)