import json
import os
import boto3
import boto3.dynamodb.conditions as conditions
from requests import get
from demo.FillUp.ServerErrorCode import ServerErrorCode
from demo.FillUp.AddFillUpRequest import AddFillUpRequest
from demo.FillUp.JSONValidationError import JSONValidationError
from demo.FillUp.ProcessingError import ProcessingError

TABLE_NAME = "FillUp"

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == "POST":
            return post_handler(event, context)
        else:
           return method_not_supported(event['httpMethod'])
    except ProcessingError as error:
        return {
            'statusCode': 400,
            'errorCode': error.errorCode,
            'message': str(error.reason)
        }
    except JSONValidationError as error:
        return {
            'statusCode': 400,
            'errorCode': ServerErrorCode.invalidInputParameters,
            'message': str(error.reason)
        }
    except:
        return {
            'statusCode': 400,
            'errorCode': 'UNKNOWN',
            'message': 'UNKNOWN'
        }

def post_handler(event, context):
    try:
        item = AddFillUpRequest.getItemJsonFrom(event['body'])
        userID = event['requestContext']['authorizer']['claims']['sub']
        insert_fillup_for_user(userID, item)
    except Exception as error:
        print(f"Error: {error}")
        raise error

    return {
            'statusCode': 200,
            'entityID': 'ID_100000000',
        }

def method_not_supported(method):
    raise ProcessingError(ServerErrorCode.unsupportedHttpMehod, f"Unsupported Method: {method}")

    # response = {}
    # items = []
    
    # try:
    #     items = get_fillUps_for_user("1")
    # except Exception as error:
    #     print(f"Error: {repr(error)}")
    # except:
    #     print("Unknown error")
    
    # response['statusCode'] = 200
    # response['items'] = items
    
    # return response

# - HELPERS

def insert_fillup_for_user(user_id: str, item: dict):
    item['userID'] = user_id
    table = get_table_resource()
    response = table.put_item(Item=item)
    verifyDynamoDbResponse(response)

def verifyDynamoDbResponse(response):
    statusCode = response['ResponseMetadata']['HTTPStatusCode']
    if response['ResponseMetadata']['HTTPStatusCode'] != statusCode:
        raise ProcessingError(ServerErrorCode.internalServerError, f"DynamoDB failed with code: {statusCode}")

def get_fillUps_for_user(user_id: str) -> list:
    table = get_table_resource()

    response = table.query(
        KeyConditionExpression=\
            conditions.Key("userID").eq(f"{user_id}")
    )
    
    return response["Items"]

def get_table_resource():
    dynamodb_resource = boto3.resource("dynamodb")
    return dynamodb_resource.Table(TABLE_NAME)