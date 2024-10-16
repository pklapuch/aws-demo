import pytest
import boto3
import os
import json
from decimal import Decimal
from moto import mock_aws
from demo.app import lambda_handler
from demo.app import TABLE_NAME
from demo.app import ServerErrorCode

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


"""
userID: userID, type: string
date: timestamp: type: string, timezone: UTC, example: 2024-06-29T13:34:30Z
cost: double, type: number; currency: USD, example: 34.12
volume: double, type: number; unit: LITER, example: 40.0
mileage: double, type: number; unit: KM: example: 113200
"""
