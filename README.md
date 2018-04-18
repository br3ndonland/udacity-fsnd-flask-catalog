# README

<a href="https://www.udacity.com/">
  <img src="https://s3-us-west-1.amazonaws.com/udacity-content/rebrand/svg/logo.min.svg" width="300" alt="Udacity logo svg">
</a>

Udacity Full Stack Web Developer Nanodegree program

[Project 4. Flask Item Catalog App](https://github.com/br3ndonland/udacity-fsnd-p4-flask-catalog)

Brendon Smith

br3ndonland

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://choosealicense.com/)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Description](#description)
- [Repository contents](#repository-contents)
- [Instructions](#instructions)
  - [Generate credentials](#generate-credentials)
  - [Install virtual machine](#install-virtual-machine)
  - [Run virtual machine](#run-virtual-machine)
  - [Run application](#run-application)

## Description

- This is a [RESTful](https://ruben.verborgh.org/blog/2012/08/24/rest-wheres-my-state/) web application created with [Python 3](https://docs.python.org/3/) and the Python micro-framework [Flask](http://flask.pocoo.org/).
- The app's [SQLite](https://sqlite.org/index.html) database contains a catalog of items and associated information. The database is created by running [database_setup.py](database_setup.py) and populated by running [database_data.py](database_data.py).
- The SQLite database is accessed by [SQLAlchemy](http://www.sqlalchemy.org/) from within the Python code in [application.py](application.py).
- The main application code is located in [application.py](application.py). This file controls the app, with Flask routing functions to render the pages of the web application and access app content.
- Authentication is performed with a hybrid flow. The [deprecated `oauth2client` library](https://google-auth.readthedocs.io/en/latest/oauth2client-deprecation.html) was used for consistency with the Udacity Vagrant virtual machine configuration. Future implementations should consider using [`google-auth`](https://google-auth.readthedocs.io/en/latest/index.html) or [`authlib`](https://docs.authlib.org/en/latest/index.html).
- Python code has been formatted according to the [PEP 8](http://pep8.org/) specification. Comments and spacing keep the code as organized and readable as possible.
- Markdown documents in the repository have been formatted in a standard style, based on suggestions from [vscode-markdownlint](https://github.com/DavidAnson/vscode-markdownlint).
- The application pages are styled with [Bootstrap 4.0.0](https://getbootstrap.com/docs/4.0/getting-started/introduction/), a library of HTML, CSS, and JavaScript components.
- The homepage displays item categories, the items most recently added to the database, and a login button.

  ![Homepage](info/img/flask-catalog-index.png)

- Clicking on a category name displays the items in the category.

  ![Category page](info/img/flask-catalog-show-category.png)

- Clicking on an item provides a photo, description, and link.

  ![Item page](info/img/flask-catalog-show-item.png)

- JSON data for each page can be accessed by clicking the JSON links on each page, which append `/json` to the URL.

  ![Homepage JSON](info/img/flask-catalog-index-json.png)

- Clicking log in allows the user to authenticate with Google.

  ![Login page](info/img/flask-catalog-login.png)

- Users who are logged in can add items, and the creator of each item can edit or delete it.

[(Back to TOC)](#table-of-contents)

## Repository contents

- [info/](info)
  - [img/](info/img) - Images used in documentation.
  - [flask-catalog-methods.md](flask-catalog-methods.md) - Step-by-step computational narrative detailing the app creation process.
  - [flask-catalog-udacity-docs.md](flask-catalog-udacity-docs.md) - Udacity documentation for the project.
- [static/](static)
  - [img/](static/img) - Images used in the main application.
- [templates/](templates) - HTML webpage templates.
- [application.py](application.py) - Main Flask app file.
- [database_data.py](database_data.py) - Python file used to populate database.
- [database_setup.py](database_setup.py) - Python file used to configure database.
- [README.md](README.md) - This file, a concise description of the project.

[(Back to TOC)](#table-of-contents)

## Instructions

### Generate credentials

- This application will require an OAuth 2.0 client ID from the Google API dashboard.
- Log into Google.
- Navigate to the [Google APIs dashboard credentials page](https://console.developers.google.com/apis/credentials).
- Click `Create credentials` and follow the prompts.
  - OAuth Client ID
  - Web application
  - Set a name. I set mine as "Brendon's Bodybuilding Bazaar".
  - Restrictions: Add `http://localhost:8000` to the Authorized JavaScript origins and Redirects.
- Download JSON and save in application directory as *client_secrets.json*.

### Install virtual machine

A virtual machine can be used to run the code from an operating system with a defined configuration. The virtual machine has all the dependencies needed to run the application.

I wrote the program in a Linux virtual machine with the following components:

- Oracle [VirtualBox](https://www.virtualbox.org/wiki/Downloads) Version 5.2.6 r120293 (Qt5.6.3)
  - Software that runs special containers called virtual machines, like Vagrant.
- [Vagrant](https://www.vagrantup.com/) 2.0.1 with Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-75-generic i686)
  - Software that provides the Linux operating system in a defined configuration, allowing it to run identically across many personal computers. Linux can then be run as a virtual machine with VirtualBox.
- [Udacity Virtual Machine configuration](https://github.com/udacity/fullstack-nanodegree-vm)
  - Repository from Udacity that configures Vagrant.
  - My personal fork of the configuration is also available on [GitHub](https://github.com/br3ndonland/fullstack-nanodegree-vm) if needed.

### Run virtual machine

- Clone the application repository into the *vagrant/* virtual machine directory.
- Start the virtual machine and log into vagrant:
  - Change into the vagrant directory on the command line (wherever you have it stored):

    ```bash
    $ cd <path>/fullstack-nanodegree-vm/vagrant
    ```

  - Start Vagrant (only necessary once per terminal session):

    ```bash
    $ vagrant up
    ```

  - Log in to Ubuntu:

    ```bash
    $ vagrant ssh
    ```

### Run application

- After logging into the virtual machine, change into the application directory:

  ```bash
  $ vagrant@vagrant:~$ cd /vagrant/flask-catalog
  ```

- Create the database:

  ```bash
  $ python3 database_setup.py
  ```

- Populate the database:

  ```bash
  $ python3 database_data.py
  ```

- Start the application:

  ```bash
  $ python3 application.py
  ```

- Navigate to [http://localhost:8000](http://localhost:8000) in a web browser. **Note that Google will reject sign-in from [http://0.0.0.0:8000](http://0.0.0.0:8000).**
- Log in, and enjoy!
- The virtual machine ssh connection can be closed with

  ```bash
  $ logout
  ```

[(Back to TOC)](#table-of-contents)