from os import environ, path

# Statement for enabling the development environment
DEBUG = bool(environ.get('FLASK_DEBUG', False))

# Define the application directory
BASE_DIR = path.abspath(path.dirname(__file__))

MONGO_URI = environ.get('MONGO_URI', 'mongodb://127.0.0.1:27017/newton')

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = environ.get('CSRF_SECRET')

# Secret key for signing cookies
SECRET_KEY = environ.get('COOKIES_SECRET')
