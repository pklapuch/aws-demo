
import json
from demo.demo.app import lambda_handler, fillUpFunction
from demo.demo.ServerErrorCode import ServerErrorCode

def test_lambda_handler_withUnsupportedMethod_devliersError():
    event = { "httpMethod": "UNKNOWN" }
    
    response = lambda_handler(event, {})
    assert response['statusCode'] == 400

    bodyJson = json.loads(response['body'])
    assert bodyJson['errorCode'] == ServerErrorCode.unsupportedHttpMehod

def test_lambda_handler_withPostMethod_invokesCreateHandler():
    postCallCountSpy = HandlerCallCountSpy()
    getCallCountSpy = HandlerCallCountSpy()
    mockCreatePostHandler(postCallCountSpy)
    mockGetPostHandler(getCallCountSpy)
    
    event = { "httpMethod": "POST" }

    assert postCallCountSpy.callCount == 0
    assert getCallCountSpy.callCount == 0

    response = lambda_handler(event, {})

    assert postCallCountSpy.callCount == 1
    assert getCallCountSpy.callCount == 0

def test_lambda_handler_withGetMethod_invokesGetHandler():
    postCallCountSpy = HandlerCallCountSpy()
    getCallCountSpy = HandlerCallCountSpy()
    mockCreatePostHandler(postCallCountSpy)
    mockGetPostHandler(getCallCountSpy)
    
    event = { "httpMethod": "GET" }

    assert postCallCountSpy.callCount == 0
    assert getCallCountSpy.callCount == 0

    response = lambda_handler(event, {})

    assert postCallCountSpy.callCount == 0
    assert getCallCountSpy.callCount == 1

# - Helpers

def mockCreatePostHandler(spy):
    def createHandlerMock(event, context):
        spy.callCount += 1
        return {}
    fillUpFunction.createHandler = createHandlerMock

def mockGetPostHandler(spy):
    def createHandlerMock(event, context):
        spy.callCount += 1
        return {}
    fillUpFunction.getHandler = createHandlerMock    

class HandlerCallCountSpy:
    def __init__(self):
        self.callCount = 0
    
    def invoke(self, event, context):
        self.callCount += 1
        return {}    