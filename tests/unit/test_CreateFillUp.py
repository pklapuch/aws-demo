import boto3
import json
from moto import mock_aws
from demo.demo.app import lambda_handler
from demo.demo.app import TABLE_NAME
from demo.demo.app import ServerErrorCode
from .Helpers.EventResourceHelper import EventResourceHelper

@mock_aws
def test_withUnsupportedHttpMethod__deliversError():
    event = { "httpMethod": "UNKNOWN" }
    
    response = lambda_handler(event, {})
    assert response['statusCode'] == 400

    bodyJson = json.loads(response['body'])
    assert bodyJson['errorCode'] == ServerErrorCode.unsupportedHttpMehod

@mock_aws
def test_createFillUp_withValidHttpMethod_andInvalidItem_deliversError():
    event = { "httpMethod": "POST" }
    
    response = lambda_handler(event, {})
    assert response['statusCode'] == 400

    bodyJson = json.loads(response['body'])
    assert bodyJson['errorCode'] == ServerErrorCode.invalidInputParameters

@mock_aws
def test_createFillUp_withValidHttpMethod_andValidItem_andWithoutAuth_deliversError():
    event = EventResourceHelper.loadEventByStringifyingBody("create_fillup_without_auth.json")
    
    response = lambda_handler(event, {})
    assert response['statusCode'] == 400

    bodyJson = json.loads(response['body'])
    assert bodyJson['errorCode'] == ServerErrorCode.invalidInputParameters

@mock_aws
def test_createFillUp_withValidHttpMethod_andValidItem_withAuth_succeeds():
    mock_table()

    event = EventResourceHelper.loadEventByStringifyingBody("create_fillup.json")

    response = lambda_handler(event, {})
    assert response['statusCode'] == 200

    bodyJson = json.loads(response['body'])
    assert bodyJson['entityID'] is not None

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
            {"AttributeName": "id", "KeyType": "RANGE"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "userID", "AttributeType": "S"},
            {"AttributeName": "id", "AttributeType": "S"}
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )

    return table
