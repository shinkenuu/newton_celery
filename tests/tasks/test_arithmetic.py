from bson import ObjectId

from pytest import fixture, raises

from constants import CALCULATION_STATUS_DONE
from tasks.arithmetic import calculate, mongo, _OPERATION_FUNCTION
from tasks.exceptions import CalculationNotFound, CalculationUpdateError


@fixture
def calculation():
    return {
        'operation': 'subtract',
        'arguments': [6, 3],
        'result': None,
        'status': 'enqueued',
    }


def test_calculate_raises_exception_when_calculation_is_not_found():
    with raises(CalculationNotFound):
        random_uuid = str(ObjectId())
        calculate(random_uuid)


def test_calculate_calls_sum_function_calculation_operation_is_sum(mocker, calculation):
    calculation['operation'] = 'sum'
    mongo.db.calculations.insert_one(calculation)

    mocked_sum = mocker.patch('tasks.arithmetic.sum_', return_value=None)
    mocker.patch.dict(_OPERATION_FUNCTION, {'sum': mocked_sum})

    calculate(str(calculation['_id']))

    mocked_sum.assert_called_once_with(*calculation['arguments'])


def test_calculate_calls_subtract_function_calculation_operation_is_subtract(mocker, calculation):
    calculation['operation'] = 'subtract'
    mongo.db.calculations.insert_one(calculation)

    mocked_subtract = mocker.patch('tasks.arithmetic.subtract', return_value=None)
    mocker.patch.dict(_OPERATION_FUNCTION, {'subtract': mocked_subtract})

    calculate(str(calculation['_id']))

    mocked_subtract.assert_called_once_with(*calculation['arguments'])


def test_calculate_calls_multiply_function_calculation_operation_is_multiply(mocker, calculation):
    calculation['operation'] = 'multiply'
    mongo.db.calculations.insert_one(calculation)

    mocked_multiply = mocker.patch('tasks.arithmetic.multiply', return_value=None)
    mocker.patch.dict(_OPERATION_FUNCTION, {'multiply': mocked_multiply})

    calculate(str(calculation['_id']))

    mocked_multiply.assert_called_once_with(*calculation['arguments'])


def test_calculate_calls_divide_function_calculation_operation_is_divide(mocker, calculation):
    calculation['operation'] = 'divide'
    mongo.db.calculations.insert_one(calculation)

    mocked_divide = mocker.patch('tasks.arithmetic.divide', return_value=None)
    mocker.patch.dict(_OPERATION_FUNCTION, {'divide': mocked_divide})

    calculate(str(calculation['_id']))

    mocked_divide.assert_called_once_with(*calculation['arguments'])


def test_calculate_persists_operation_result_and_done_status(calculation):
    mongo.db.calculations.insert_one(calculation)

    calculate(str(calculation['_id']))

    persisted_calculation = mongo.db.calculations.find_one({'_id': calculation['_id']})

    expected_result = 3
    assert persisted_calculation['result'] == expected_result

    expected_status = CALCULATION_STATUS_DONE
    assert persisted_calculation['status'] == expected_status


def test_calculate_persists_arithmetic_error_description_in_calculation_status(calculation):
    calculation['operation'] = 'divide'
    calculation['arguments'] = [1, 0]

    mongo.db.calculations.insert_one(calculation)

    calculate(str(calculation['_id']))

    persisted_calculation = mongo.db.calculations.find_one({'_id': calculation['_id']})

    expected_status = 'division by zero'
    assert persisted_calculation['status'] == expected_status


def test_calculate_persists_error_status_when_exception_is_raised(mocker, calculation):
    calculation['operation'] = 'sum'
    mongo.db.calculations.insert_one(calculation)

    mocked_sum = mocker.patch('tasks.arithmetic.sum_', side_effect=Exception)
    mocker.patch.dict(_OPERATION_FUNCTION, {'sum': mocked_sum})

    calculate(str(calculation['_id']))

    persisted_calculation = mongo.db.calculations.find_one({'_id': calculation['_id']})

    expected_status = 'error'
    assert persisted_calculation['status'] == expected_status


def test_calculate_raises_exception_when_persistence_fails(mocker, calculation):
    mongo.db.calculations.insert_one(calculation)

    class FakeUpdateResult:
        acknowledged = False

    fake_update_result = FakeUpdateResult()

    mocker.patch('pymongo.collection.Collection.update_one', return_value=fake_update_result)

    with raises(CalculationUpdateError):
        calculate(str(calculation['_id']))
