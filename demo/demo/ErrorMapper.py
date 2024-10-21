import json
from .JSONValidationError import JSONValidationError
from .ServerErrorCode import ServerErrorCode
from .ProcessingError import ProcessingError

def mapErrorToResponse(error):
    statusCode = 400
    body = {}

    if isinstance(error, JSONValidationError):
        body =  {
            'errorCode': ServerErrorCode.invalidInputParameters,
            'message': str(error.reason)
        }
    elif isinstance(error, ProcessingError):
        body =  {
            'errorCode': error.errorCode,
            'message': str(error.reason)
        }
    else:
        body =  {
            'errorCode': 'UNKNOWN',
            'message': f'{error}'
        }
    
    return {
        'statusCode': statusCode,
        'body': json.dumps(body)
    }