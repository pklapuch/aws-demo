import pytest
import boto3
import os
from moto import mock_aws
from demo.app import lambda_handler
from demo.app import ENV_TABLE_NAME

TABLE_NAME = "FillUp"

@pytest.fixture
def lambda_environment():
    os.environ[ENV_TABLE_NAME] = TABLE_NAME

def mock_database(item):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "userID", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "userID", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"}
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    table.put_item(Item=item)

@mock_aws
def test_lambda_handler(lambda_environment):
    """On successful execution returns all stored items"""
    
    storedItem = {
        "userID": "1",
        "SK": "test",
        "fillup": "test",
    }

    mock_database(storedItem)

    response = lambda_handler({}, {})
    print(response)
    
    statusCode = response['statusCode']
    assert statusCode == 200

    items = response['items']
    assert items == [storedItem]