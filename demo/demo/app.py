from .ProcessingError import ProcessingError
from .ServerErrorCode import ServerErrorCode
from .CreateFillUpHandler import CreateFillUpHandler
from .GetFillUpHandler import GetFillUpHandler
from .ErrorMapper import mapErrorToResponse

class FillUpFunction:
    createHandler = CreateFillUpHandler().create_handler
    getHandler = GetFillUpHandler().get_handler

fillUpFunction = FillUpFunction()

def lambda_handler(event, context):
    print(event)

    try:
        method = event['httpMethod']

        if method == "POST":
            return fillUpFunction.createHandler(event, context)
        elif method == "GET":
            return fillUpFunction.getHandler(event, context)
        else:
           return method_not_supported(event['httpMethod'])
    except Exception as error:
        return mapErrorToResponse(error)

def method_not_supported(method):
    raise ProcessingError(ServerErrorCode.unsupportedHttpMehod, f"Unsupported Method: {method}")