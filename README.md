# README

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
</a>

**Udacity Full Stack Web Developer Nanodegree program**

[Project 4. Flask Item Catalog App](https://github.com/br3ndonland/udacity-fsnd-p4-flask-catalog)

Brendon Smith

br3ndonland

## TOC
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Description](#description)
- [Repository contents](#repository-contents)
- [Development environment](#development-environment)
- [Application](#application)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Description

* This is a [RESTful](https://ruben.verborgh.org/blog/2012/08/24/rest-wheres-my-state/) web application created with [Python 3](https://docs.python.org/3/) and the Python micro-framework [Flask](http://flask.pocoo.org/).
* The app's SQLite database contains a catalog of items and associated information. 
* The SQLite database is accessed by [SQLAlchemy](http://www.sqlalchemy.org/) from within the Python code in [application.py](application.py).
* The main application code is located in [application.py](application.py). This file controls the app with routing functions to render the pages of the web application and access app content. The Python code conforms to the [PEP 8](http://pep8.org/) specification. Comments and spacing keep the code as organized and readable as possible.
* The web pages are styled with [Bootstrap 4.0.0](https://getbootstrap.com/docs/4.0/getting-started/introduction/), a library of HTML, CSS, and JavaScript components.

The homepage displays item categories, the items most recently added to the database, and a login button.

<img src="static/img/flask-catalog-home.png" alt="Homepage">

Clicking log in allows the user to authenticate with Google.

<img src="static/img/flask-catalog-login.png" alt="Login page">

Clicking on a category name displays the items in the category.

<img src="static/img/flask-catalog-categories.png" alt="Page for categories">

Clicking on an item provides a photo, description, and link. Users who are logged in can add items, and the creator of each item can edit or delete it.

<img src="static/img/flask-catalog-item.png" alt="Pages for individual items">


## Repository contents

* *docs/*: Project documentation
	- [flask-catalog-methods.md](flask-catalog-methods.md): Step-by-step computational narrative detailing the app creation process
	- [flask-catalog-udacity-docs.md](flask-catalog-udacity-docs.md): Udacity documentation for the project
* *static/*: Static CSS, JavaScript, and image files for the app.
	- css/
	- img/
	- js/
* *templates/*: HTML webpage templates
* [application.py](application.py): Main Flask app file
* [database_data.py](database_data.py): Python file used to populate database
* [database_setup.py](database_setup.py): Python file used to configure database
* [README.md](README.md): This file, a concise description of the project


## Development environment

A virtual machine can be used to run the code from an operating system with a defined configuration. The virtual machine has all the dependencies needed to run the app.

I wrote the program in a Linux virtual machine with the following components:

* Oracle [VirtualBox](https://www.virtualbox.org/wiki/Downloads) Version 5.2.6 r120293 (Qt5.6.3)
	- Software that runs special containers called virtual machines, like Vagrant.
* [Vagrant](https://www.vagrantup.com/) 2.0.1 with Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-75-generic i686)
	- Software that provides the Linux operating system in a defined configuration, allowing it to run identically across many personal computers. Linux can then be run as a virtual machine with VirtualBox.
* [Udacity Virtual Machine configuration](https://github.com/udacity/fullstack-nanodegree-vm)
	- Repository from Udacity that configures Vagrant.


## Application

* Save the application repository within the */vagrant/* virtual machine directory.
* Start the virtual machine and log into vagrant:
	- Change into the vagrant directory on the command line (wherever you have it stored):
		```bash
		$ cd <path>/fullstack-nanodegree-vm/vagrant
		```
	- Start Vagrant (only necessary after computer restart):
		```bash
		$ vagrant up
		```
	- Log in to Ubuntu:
		```bash
		$ vagrant ssh
		```
* Change into the application directory:
	```bash
	$ vagrant@vagrant:~$ cd /vagrant/flask-catalog
	```
* Create the database:
	```bash
	$ python3 database_setup.py
	```
* Populate the database:
	```bash
	$ python3 database_data.py
	```
* Start the application:
	```bash
	$ python3 application.py
	```
* Navigate to http://localhost:8000 in a web browser.
* Log in, and enjoy!

[(Back to TOC)](#toc)