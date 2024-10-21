from .ProcessingError import ProcessingError
from .ServerErrorCode import ServerErrorCode
from .CreateFillUpHandler import create_handler
from .GetFillUpHandler import get_handler
from .ErrorMapper import mapErrorToResponse

def lambda_handler(event, context):
    print(event)

    try:
        method = event['httpMethod']

        if method == "POST":
            return create_handler(event, context)
        elif method == "GET":
            return get_handler(event, context)
        else:
           return method_not_supported(event['httpMethod'])
    except Exception as error:
        return mapErrorToResponse(error)

def method_not_supported(method):
    raise ProcessingError(ServerErrorCode.unsupportedHttpMehod, f"Unsupported Method: {method}")