import json
from .EventUtility import EventUtility
from .DynamoDbUtility import DynamoDbUtility
from .AddFillUpRequest import AddFillUpRequest
from uuid import uuid4

TABLE_NAME = "FillUp"

def create_handler(event: dict, context):
    userID = EventUtility.extract_user_id(event)
    body = EventUtility.extract_body(event)
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

def insert_fillup_for_user(id: str, user_id: str, addRequest: AddFillUpRequest):
    item = addRequest.toDynamoDbInsertDict(id, user_id)
    table = DynamoDbUtility.get_table_resource(TABLE_NAME)
    response = table.put_item(Item=item)
    DynamoDbUtility.verify_response(response)    