import json
import os
import boto3
import boto3.dynamodb.conditions as conditions

ENV_TABLE_NAME = "TABLE_NAME"

def get_table_resource():
    dynamodb_resource = boto3.resource("dynamodb")
    table_name = os.environ[ENV_TABLE_NAME]
    return dynamodb_resource.Table(table_name)

def get_fillUps_for_user(user_id: str) -> list:
    print("TABLE NAME: " + os.environ[ENV_TABLE_NAME])
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