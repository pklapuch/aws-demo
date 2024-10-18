from moto import mock_aws
from demo.demo.app import lambda_handler
from demo.demo.FillUp import FillUp
from .Helpers.FillUpMockHelper import FillUpMockHelper
from .Helpers.EventResourceHelper import EventResourceHelper
from decimal import Decimal
import json
import json
import json

@mock_aws
def test_createFillUp_withValidHttpMethod_andValidItem_withAuth_succeeds():
    userID = "mock_user_id"
    storedItem = makeTestFillUp(userID)
    FillUpMockHelper.create_table_with_item(storedItem.encodeAsDynamoDbDict())

    event = EventResourceHelper.loadEventByStringifyingBody("get_fillups.json")
    eventWithAuth = EventResourceHelper.insertUserIdentity(event, userID)

    response = lambda_handler(eventWithAuth, {})
    assert response["statusCode"] == 200

    receivedItems = json.loads(response["body"])
    assert len(receivedItems) == 1

    receivedItem = FillUp.decodeFromJSON(receivedItems[0])
    assert receivedItem == storedItem

# - HELPERS

def makeTestFillUp(userID: str):
    return FillUp(
        "item_id",
        userID,
        "2024-06-29T13:34:30Z",
        34.12,
        40.0,
        113200.8
    )
