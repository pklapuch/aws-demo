import json
import os
import boto3
import boto3.dynamodb.conditions as conditions

TABLE_NAME = "FillUp"

def get_table_resource():
    dynamodb_resource = boto3.resource("dynamodb")
    return dynamodb_resource.Table(TABLE_NAME)

def get_fillUps_for_user(user_id: str) -> list:
    table = get_table_resource()

    response = table.query(
        KeyConditionExpression=\
            conditions.Key("userID").eq(f"{user_id}")
    )
    
    return response["Items"]

def lambda_handler(event, context):
    response = {}
    items = []
    
    try:
        items = get_fillUps_for_user("1")
    except Exception as error:
        print(f"Error: {repr(error)}")
    except:
        print("Unknown error")
    
    response['statusCode'] = 200
    response['items'] = items
    
    return response

