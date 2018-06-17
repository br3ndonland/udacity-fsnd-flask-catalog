# Add path to application directory
import sys
sys.path.insert(0, "/var/www/catalog")

# Import Flask instance from main application file
from application import app as application

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=8000)
