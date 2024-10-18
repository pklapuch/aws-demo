import json
from uuid import uuid4
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
    except Exception as error:
        return mapErrorToResponse(error)
    
def mapErrorToResponse(error):
    statusCode = 400
    body = {}

    if isinstance(error, JSONValidationError):
        body =  {
            'errorCode': ServerErrorCode.invalidInputParameters,
            'message': str(error.reason)
        }
    elif isinstance(error, ProcessingError):
        body =  {
            'errorCode': error.errorCode,
            'message': str(error.reason)
        }
    else:
        body =  {
            'errorCode': 'UNKNOWN',
            'message': 'UNKNOWN'
        }
    
    return {
        'statusCode': statusCode,
        'body': json.dumps(body)
    }

def post_handler(event, context):
    userID = extract_user_id(event)
    body = extract_body(event)
    addRequest = AddFillUpRequest.decode(body)
    id = str(uuid4())
    insert_fillup_for_user(id, userID, addRequest)

    body = {
        'entityID': id,
    }

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

def method_not_supported(method):
    raise ProcessingError(ServerErrorCode.unsupportedHttpMehod, f"Unsupported Method: {method}")

# - HELPERS

def insert_fillup_for_user(id: str, user_id: str, addRequest: AddFillUpRequest):
    item = addRequest.toDynamoDbInsertDict(id, user_id)
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
    return json.loads(event['body'])

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