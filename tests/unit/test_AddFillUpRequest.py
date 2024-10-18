from collections import namedtuple
from decimal import Decimal
from demo.demo.AddFillUpRequest import AddFillUpRequest
from demo.demo.JSONValidationError import JSONValidationError

def test_decode_withValidJson_deliversItem():
    testBundle = load_testBundle()
    model = AddFillUpRequest.decode(testBundle.json)
    assert model == testBundle.model

def test_toDynamoDbInsertDict_deliversDynamoDbInsertDictionary():
    id = 'entityID'
    userID = 'mock_user'
    testBundle = load_testBundle()
    dynamoDbInsertDict = testBundle.model.toDynamoDbInsertDict(id, userID)

    assert dynamoDbInsertDict['id'] == id
    assert dynamoDbInsertDict['userID'] == userID
    assert dynamoDbInsertDict['kilometers'] == Decimal(str(testBundle.model.kilometers))
    assert dynamoDbInsertDict['liters'] == Decimal(str(testBundle.model.liters))
    assert dynamoDbInsertDict['cost'] == Decimal(str(testBundle.model.cost))

def test_decode_withInvalidJson_throwsException():
    json = {}
    
    try:
        AddFillUpRequest.decode(json)
        assert False
    except JSONValidationError as error:
        assert True
    except: 
        assert False

# - HELPERS    
    
TestBundle = namedtuple('TestBundle', ['json', 'model'])    
def load_testBundle():
    json = {
        "date": "2024-06-29T13:34:30Z",
        "kilometers": 100.3,
        "liters": 30.3,
        "cost": 25.2
    }

    model = AddFillUpRequest(
        "2024-06-29T13:34:30Z",
        100.3,
        30.3,
        25.2
    )

    return TestBundle(json, model)