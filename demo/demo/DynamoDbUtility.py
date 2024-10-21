import boto3
from .ProcessingError import ProcessingError
from .ServerErrorCode import ServerErrorCode

class DynamoDbUtility:

    @staticmethod
    def get_table_resource(tableName):
        resource = boto3.resource("dynamodb")
        return resource.Table(tableName)

    @staticmethod
    def verify_response(response):
        statusCode: int
        
        try:
            statusCode = response['ResponseMetadata']['HTTPStatusCode']
        except:
            raise ProcessingError(ServerErrorCode.internalServerError, f"DynamoDB invalid response")
        
        if response['ResponseMetadata']['HTTPStatusCode'] != statusCode:
            raise ProcessingError(ServerErrorCode.internalServerError, f"DynamoDB failed with code: {statusCode}")

