import pytest
import boto3
import os
from moto import mock_aws
from demo.app import lambda_handler
from demo.app import TABLE_NAME

@mock_aws
def test_lambda_handler():
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

# - HELPERS

def mock_database(item):
    table = mock_table();
    table.put_item(Item=item)

def mock_table():
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

    return table