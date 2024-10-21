import json
from moto import mock_aws
from demo.demo.app import lambda_handler
from demo.demo.CreateFillUpHandler import TABLE_NAME
from demo.demo.app import ServerErrorCode
from .Helpers.EventResourceHelper import EventResourceHelper
from .Helpers.FillUpMockHelper import FillUpMockHelper

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
    FillUpMockHelper.create_table(TABLE_NAME)

    event = EventResourceHelper.loadEventByStringifyingBody("create_fillup.json")

    response = lambda_handler(event, {})
    assert response['statusCode'] == 200

    bodyJson = json.loads(response['body'])
    assert bodyJson['entityID'] is not None