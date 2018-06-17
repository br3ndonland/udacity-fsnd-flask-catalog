# Enable use of virtual environment with mod_wsgi
activate_this = '/home/grader/.local/share/virtualenvs/catalog-1BsMKvn0/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
# Add path to application directory
sys.path.insert(0, "/var/www/catalog")

# Import Flask instance from main application file
from application import app as application

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=8000)
