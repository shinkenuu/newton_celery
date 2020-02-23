import logging
from bson import ObjectId

from app import mongo
from arithmetic import sum_, subtract, multiply, divide
from constants import (
    SUM_OPERATION_NAME,
    SUBTRACT_OPERATION_NAME,
    MULTIPLY_OPERATION_NAME,
    DIVIDE_OPERATION_NAME,
    CALCULATION_STATUS_DONE,
    CALCULATION_STATUS_ERROR,
)
from tasks import celery_app
from tasks.exceptions import CalculationNotFound, CalculationUpdateError

_OPERATION_FUNCTION = {
    SUM_OPERATION_NAME: sum_,
    SUBTRACT_OPERATION_NAME: subtract,
    MULTIPLY_OPERATION_NAME: multiply,
    DIVIDE_OPERATION_NAME: divide,
}


@celery_app.task
def calculate(calculation_uuid: str):
    logging.info('Processing calculation with uuid: %s', calculation_uuid)

    _id = ObjectId(calculation_uuid)
    calculation = mongo.db.calculations.find_one({'_id': _id})
    result = None
    status = None

    if not calculation:
        raise CalculationNotFound(calculation_uuid)

    try:
        operation_function = _OPERATION_FUNCTION[calculation['operation']]
        result = operation_function(*calculation['arguments'])
        status = CALCULATION_STATUS_DONE

    except ArithmeticError as error:
        logging.error(error)
        status = str(error)

    except Exception as exception:
        logging.error(exception)
        status = CALCULATION_STATUS_ERROR

    finally:
        logging.info('Calculation with uuid %s finished', calculation_uuid)

        update_result = mongo.db.calculations.update_one(
            {'_id': _id},
            {'$set': {
                'result': result,
                'status': status,
            }},
            upsert=False
        )

        if not update_result.acknowledged:
            raise CalculationUpdateError(str(calculation))
