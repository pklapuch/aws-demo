import json
from .EventUtility import EventUtility
from .DynamoDbUtility import DynamoDbUtility
import boto3.dynamodb.conditions as conditions
from .FillUp import FillUp

TABLE_NAME = "FillUp"

class GetFillUpHandler:

    def get_handler(self, event: dict, context):
        userID = EventUtility.extract_user_id(event)
        fillUps = self.get_fillUps_for_user(userID)

        return {
            'statusCode': 200,
            'body': json.dumps(fillUps)
        }

    def get_fillUps_for_user(self, user_id: str) -> list:
        table = DynamoDbUtility.get_table_resource(TABLE_NAME)

        dynamoDbResponse = table.query(
            KeyConditionExpression=\
                conditions.Key("userID").eq(f"{user_id}")
        )

        DynamoDbUtility.verify_response(dynamoDbResponse)
        dynamoDbItems = dynamoDbResponse["Items"]
        fillUps = list(map(FillUp.decodeFromDynamoDbDict, dynamoDbItems))
        return list(map(lambda obj: obj.encodeAsJSON(), fillUps))