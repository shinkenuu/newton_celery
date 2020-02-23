from bson import ObjectId

from pytest import fixture

from views import (
    calculate,
    mongo,
)


@fixture
def calculation_payload():
    return {
        'operation': 'subtract',
        'arguments': [6, 3],
    }


@fixture
def enqueued_calculation():
    return {
        'operation': 'subtract',
        'arguments': [6, 3],
        'result': None,
        'status': 'enqueued',
    }


_CALCULATIONS_LIST_PATH = '/calculations'
_CALCULATIONS_DETAIL_PATH = '/calculations/{uuid}'


def test_calculation_detail_get_returns_200_and_specified_calculation_when_found(client, enqueued_calculation):
    mongo.db.calculations.insert_one(enqueued_calculation)

    url = _CALCULATIONS_DETAIL_PATH.format(uuid=str(enqueued_calculation['_id']))
    response = client.get(url)

    assert response.status_code == 200

    del enqueued_calculation['_id']
    assert response.json == enqueued_calculation


def test_calculation_detail_get_returns_404_when_not_found(client, enqueued_calculation):
    mongo.db.calculations.insert_one(enqueued_calculation)

    url = _CALCULATIONS_DETAIL_PATH.format(uuid=str(ObjectId()))
    response = client.get(url)

    assert response.status_code == 404


def test_calculation_list_post_returns_201_when_calculation_is_created(
        client, mocker, calculation_payload, enqueued_calculation):
    mocker.patch.object(calculate, 'delay')

    response = client.post(_CALCULATIONS_LIST_PATH, json=calculation_payload)

    assert response.status_code == 201

    persisted_calculation = mongo.db.calculations.find_one({'_id': ObjectId(response.json['uuid'])})

    assert persisted_calculation is not None

    del persisted_calculation['_id']
    assert persisted_calculation == enqueued_calculation


def test_calculation_list_post_schedules_requested_calculation(
        client, mocker, calculation_payload):
    mocked_calculate_delay = mocker.patch.object(calculate, 'delay')

    response = client.post(_CALCULATIONS_LIST_PATH, json=calculation_payload)

    assert response.status_code == 201
    mocked_calculate_delay.assert_called_once_with(response.json['uuid'])


def test_calculation_list_post_returns_400_when_payload_arguments_contains_less_than_2_items(
        client, mocker, calculation_payload):
    mocker.patch.object(calculate, 'delay')

    calculation_payload['arguments'] = [1]
    response = client.post(_CALCULATIONS_LIST_PATH, json=calculation_payload)

    assert response.status_code == 400

    expected_response_json = {
        'error': {
            'arguments': ['Shorter than minimum length 2.'],
        }
    }
    assert response.json == expected_response_json


def test_calculation_list_post_returns_400_when_payload_operation_doesnt_match_the_registered(
        client, mocker, calculation_payload):
    mocker.patch.object(calculate, 'delay')

    calculation_payload['operation'] = 'factorial'
    response = client.post(_CALCULATIONS_LIST_PATH, json=calculation_payload)

    assert response.status_code == 400

    expected_response_json = {
        'error': {
            'operation': ['Must be one of: sum, subtract, multiply, divide.'],
        }
    }
    assert response.json == expected_response_json


def test_calculation_list_post_returns_500_when_calculation_persistence_failed(
        client, mocker, calculation_payload):
    mocker.patch.object(calculate, 'delay')

    class FakeInsertResult:
        acknowledged = False

    fake_insert_result = FakeInsertResult()

    mocker.patch('pymongo.collection.Collection.insert_one', return_value=fake_insert_result)
    response = client.post(_CALCULATIONS_LIST_PATH, json=calculation_payload)

    assert response.status_code == 500


def test_calculation_list_post_returns_500_when_calculation_schedule_failed(
        client, mocker, calculation_payload):
    mocker.patch.object(calculate, 'delay', side_effect=Exception)

    response = client.post(_CALCULATIONS_LIST_PATH, json=calculation_payload)

    assert response.status_code == 500
