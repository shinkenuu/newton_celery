from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo

app = Flask('web')
app.config.from_object('config')

api = Api(app)
mongo = PyMongo(app)

from views import CalculationDetailResource, CalculationListResource

api.add_resource(CalculationListResource, '/calculations')
api.add_resource(CalculationDetailResource, '/calculations/<string:uuid>')
