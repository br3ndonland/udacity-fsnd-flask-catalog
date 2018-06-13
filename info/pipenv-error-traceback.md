# Conda update problem

- Couldn't run the pipenv on 20180611 after updating to conda 4.5.4 and Python 3.6.5
- Flask was also updated to 1.0.2, but the problem doesn't seem to be with Flask.
- Seems to be with the Python namespace

  ```text
  (udacity-fsnd-p4-flask-catalog-JlX-3R7E) $ python3 application.py
  Traceback (most recent call last):
    File "application.py", line 17, in <module>
      from flask import Flask, flash, jsonify, make_response, redirect
    File "/Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/site-packages/flask/__init__.py", line 19, in <module>
      from jinja2 import Markup, escape
    File "/Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/site-packages/jinja2/__init__.py", line 82, in <module>
      _patch_async()
    File "/Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/site-packages/jinja2/__init__.py", line 78, in _patch_async
      from jinja2.asyncsupport import patch_all
    File "/Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/site-packages/jinja2/asyncsupport.py", line 13, in <module>
      import asyncio
    File "/Users/br3ndonland/anaconda3/lib/python3.6/asyncio/__init__.py", line 21, in <module>
      from .base_events import *
    File "/Users/br3ndonland/anaconda3/lib/python3.6/asyncio/base_events.py", line 17, in <module>
      import concurrent.futures
    File "/Users/br3ndonland/anaconda3/lib/python3.6/concurrent/futures/__init__.py", line 17, in <module>
      from concurrent.futures.process import ProcessPoolExecutor
    File "/Users/br3ndonland/anaconda3/lib/python3.6/concurrent/futures/process.py", line 55, in <module>
      from multiprocessing.connection import wait
    File "/Users/br3ndonland/anaconda3/lib/python3.6/multiprocessing/connection.py", line 23, in <module>
      from . import util
    File "/Users/br3ndonland/anaconda3/lib/python3.6/multiprocessing/util.py", line 17, in <module>
      from subprocess import _args_from_interpreter_flags
    File "/Users/br3ndonland/anaconda3/lib/python3.6/subprocess.py", line 136, in <module>
      import _posixsubprocess
  ImportError: dlopen(/Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/lib-dynload/_posixsubprocess.cpython-36m-darwin.so, 2): Symbol not found: __Py_set_inheritable_async_safe
    Referenced from: /Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/lib-dynload/_posixsubprocess.cpython-36m-darwin.so
    Expected in: flat namespace
  in /Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/lib-dynload/_posixsubprocess.cpython-36m-darwin.so
  ```

- similar error with pipenv update

  ```text
  (udacity-fsnd-p4-flask-catalog-JlX-3R7E) br3ndonland udacity-fsnd-p4-flask-catalog
  $ pipenv update
  Running $ pipenv lock then $ pipenv sync.
  Locking [dev-packages] dependencies…
  6/platform.py", line 116, in <module>
      import sys, os, re, subprocess
    File "/Users/br3ndonland/anaconda3/lib/python3.6/subprocess.py", line 136, in <module>
      import _posixsubprocess
  ImportError: dlopen(/Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/lib-dynload/_posixsubprocess.cpython-36m-darwin.so, 2): Symbol not found: __Py_set_inheritable_async_safe
    Referenced from: /Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/lib-dynload/_posixsubprocess.cpython-36m-darwin.so
    Expected in: flat namespace
  in /Users/br3ndonland/.local/share/virtualenvs/udacity-fsnd-p4-flask-catalog-JlX-3R7E/lib/python3.6/lib-dynload/_posixsubprocess.cpython-36m-darwin.so
  ```

- Ran `hash -r python`. Restarted. No improvement.
- Based on [this](https://groups.google.com/forum/#!topic/theano-users/0Jthageb384) I should reinstall Apple command line tools.