import boto3
import json
from decimal import Decimal
from moto import mock_aws
from demo.demo.app import lambda_handler
from demo.demo.app import TABLE_NAME
from demo.demo.app import ServerErrorCode

@mock_aws
def test_withUnsupportedHttpMethod__deliversError():
    event = { "httpMethod": "UNKNOWN" }
    response = lambda_handler(event, {})
    print(f"Respnse: {response}")

    assert response['statusCode'] == 400
    assert response['errorCode'] == ServerErrorCode.unsupportedHttpMehod

@mock_aws
def test_createFillUp_withValidHttpMethod_andInvalidItem_deliversError():
    event = { "httpMethod": "POST" }
    print(f"Event: {event}")

    response = lambda_handler(event, {})
    print(f"Respnse: {response}")

    assert response['statusCode'] == 400
    assert response['errorCode'] == ServerErrorCode.invalidInputParameters

@mock_aws
def test_createFillUp_withValidHttpMethod_andValidItem_succeeds():
    mock_table()

    event = loadEvent("create_fillup.json")
    print(f"Event: {event}")

    response = lambda_handler(event, {})
    print(f"Respnse: {response}")

    assert response['statusCode'] == 200

def loadEvent(name: str):
    with open(f"events/{name}", 'r') as file:
        return json.load(file)

# - HELPERS

def mock_database(item):
    table = mock_table()
    table.put_item(Item=item)

def mock_table():
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "userID", "KeyType": "HASH"},
            {"AttributeName": "date", "KeyType": "RANGE"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "userID", "AttributeType": "S"},
            {"AttributeName": "date", "AttributeType": "S"}
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )

    return table
