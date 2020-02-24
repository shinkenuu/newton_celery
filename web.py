import logging
from os import environ

from app import app

logging.basicConfig(level=logging.INFO)

HOST = environ.get('WEB_HOST', '0.0.0.0')
PORT = int(environ.get('WEB_PORT', 5000))

app.run(host=HOST, port=PORT)
