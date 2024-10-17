import boto3
import boto3.dynamodb.conditions as conditions
from decimal import Decimal

from .ServerErrorCode import ServerErrorCode
from .AddFillUpRequest import AddFillUpRequest
from .JSONValidationError import JSONValidationError
from .ProcessingError import ProcessingError

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
        body = extract_body(event)
        item = AddFillUpRequest.decode(body)
        userID = extract_user_id(event)
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

# - HELPERS

def insert_fillup_for_user(user_id: str, addRequest: AddFillUpRequest):
    item = addRequest.toDynamoDbInsertDict(user_id)
    table = get_table_resource()
    response = table.put_item(Item=item)
    verifyDynamoDbResponse(response)

def verifyDynamoDbResponse(response):
    statusCode: int
    
    try:
        statusCode = response['ResponseMetadata']['HTTPStatusCode']
    except:
        raise ProcessingError(ServerErrorCode.internalServerError, f"DynamoDB invalid response")
    
    if response['ResponseMetadata']['HTTPStatusCode'] != statusCode:
        raise ProcessingError(ServerErrorCode.internalServerError, f"DynamoDB failed with code: {statusCode}")

def extract_body(event):
    try:
        return event['body']
    except:
        raise JSONValidationError("`body` not set!")

def extract_user_id(event):
    try:
        return event['requestContext']['authorizer']['claims']['sub']
    except:
        raise JSONValidationError("`userID` not set!")
    
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