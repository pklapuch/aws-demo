import boto3
from demo.demo.app import TABLE_NAME

class FillUpMockHelper:
    @staticmethod
    def create_table_with_item(item):
        table = FillUpMockHelper.create_table()
        table.put_item(Item=item)

    @staticmethod
    def create_table():
        dynamodb_resource = boto3.resource("dynamodb")
        table = dynamodb_resource.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "userID", "KeyType": "HASH"},
                {"AttributeName": "id", "KeyType": "RANGE"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "userID", "AttributeType": "S"},
                {"AttributeName": "id", "AttributeType": "S"}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

        return table
