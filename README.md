# README

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

- [Project description](#project-description)
- [Repository contents](#repository-contents)
- [Development environment](#development-environment)
- [Application](#application)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Project description

RESTful Python Flask web app with CRUD and OAuth


## Repository contents

* docs/
	- [flask-catalog-methods.md](flask-catalog-methods.md): Step-by-step computational narrative detailing the app creation process
	- [flask-catalog-udacity-docs.md](flask-catalog-udacity-docs.md): Udacity documentation for the project
* static/
	- css/
	- js/
* templates/
	- HTML webpage templates
* [application.py](application.py): Main Flask app
* [database_setup.py](database_setup.py): Python file used to configure database
* [README.md](README.md): This file, a concise description of the project


## Development environment

### Application dependencies

* Flask
* Python 3
* SQLAlchemy


### Virtual machine

A virtual machine can be used to run the code from an operating system with a defined configuration. The virtual machine has all the dependencies needed to run the app.


#### Virtual machine configuration

I wrote the program in a Linux virtual machine with the following components:

* Oracle [VirtualBox](https://www.virtualbox.org/wiki/Downloads) Version 5.2.6 r120293 (Qt5.6.3)
	- Software that runs special containers called  virtual machines, like Vagrant.
* [Vagrant](https://www.vagrantup.com/) 2.0.1 with Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-75-generic i686)
	- Software that provides the Linux operating system in a defined configuration, allowing it to run identically across many personal computers. Linux can then be run as a virtual machine with VirtualBox.
* [Udacity Virtual Machine configuration](https://github.com/udacity/fullstack-nanodegree-vm)
	- Repository from Udacity that configures Vagrant.
	- I created a directory at */vagrant/flask-catalog* for the application.


#### Virtual machine operation

On the Linux command line:

Change into the Vagrant directory (wherever you have it stored):

```bash
$ cd <path>/fullstack-nanodegree-vm/vagrant
```

Start Vagrant (only necessary after computer restart):

```bash
$ vagrant up
```

Log in to Ubuntu:

```bash
$ vagrant ssh
```


## Application

Save the application at */vagrant/flask-catalog*.

On the Linux command line, after logging into vagrant:

Change into the application directory:

```bash
$ vagrant@vagrant:~$ cd /vagrant/flask-catalog
```

Set up the database:

```bash
$ python3 database_setup.py
```

Start the application:

```bash
$ python3 project.py
```

Navigate to http://localhost:8000 in a web browser.

Log in, and enjoy!

[(back to top)](#top)