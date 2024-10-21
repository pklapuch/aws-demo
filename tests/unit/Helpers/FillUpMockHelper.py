import boto3

class FillUpMockHelper:
    @staticmethod
    def create_table_with_item(item, tableName):
        table = FillUpMockHelper.create_table(tableName)
        table.put_item(Item=item)

    @staticmethod
    def create_table(tableName):
        dynamodb_resource = boto3.resource("dynamodb")
        table = dynamodb_resource.create_table(
            TableName=tableName,
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
