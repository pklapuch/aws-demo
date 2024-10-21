import json
from .ProcessingError import ProcessingError
from .ServerErrorCode import ServerErrorCode

class EventUtility:

    @staticmethod
    def extract_user_id(event):
        try:
            return event['requestContext']['authorizer']['claims']['sub']
        except:
            raise ProcessingError(ServerErrorCode.invalidInputParameters, "`user identity` not set!")


    @staticmethod
    def extract_body(event: dict):
        return json.loads(event['body'])