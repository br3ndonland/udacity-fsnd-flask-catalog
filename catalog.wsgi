# Enable use of virtual environment with mod_wsgi
activate_this = '/var/www/catalog/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Flask instance from main application file
from application import app as application
