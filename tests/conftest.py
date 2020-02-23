from flask_pymongo import PyMongo
import pytest

from app import app as flask_app


@pytest.fixture(scope='session')
def app(request):
    flask_app.config['TESTING'] = True
    flask_app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/newton_test'

    # Establish an application context before running the tests.
    context = flask_app.app_context()
    context.push()

    def teardown():
        context.pop()

    request.addfinalizer(teardown)
    return flask_app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
