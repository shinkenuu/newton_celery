from bson import ObjectId
import logging

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app import mongo
from constants import CALCULATION_STATUS_ENQUEUED
from schemas import CalculationSchema


class CalculationListResource(Resource):
    schema = CalculationSchema()

    def post(self):
        from tasks.arithmetic import calculate  # TODO: toplevel import is breaking

        try:
            calculation = self.schema.load(request.json)
            calculation['result'] = None
            calculation['status'] = CALCULATION_STATUS_ENQUEUED

            insertion_result = mongo.db.calculations.insert_one(calculation)

            if not insertion_result.acknowledged:
                logging.error('Error inserting %s', str(calculation))
                return {'error': 'internal error'}, 500

            uuid = str(insertion_result.inserted_id)
            calculate.delay(uuid)

            return {'uuid': uuid}, 201

        except ValidationError as error:
            return {'error': error.messages}, 400

        except Exception as exception:
            logging.error(exception)
            return {'error': 'internal error'}, 500


class CalculationDetailResource(Resource):
    schema = CalculationSchema()

    def get(self, uuid):
        calculation = mongo.db.calculations.find_one({'_id': ObjectId(uuid)})

        if not calculation:
            return '', 404

        serialized_calculation = self.schema.dump(calculation)
        return serialized_calculation, 200
