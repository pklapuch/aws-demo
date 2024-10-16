import pytest
from demo.FillUp.AddFillUpRequest import AddFillUpRequest

def test_parseJson_withValidJson_deliversItem():
    modelJson = {
        "date": "2024-06-29T13:34:30Z",
        "kilometers": 100.3,
        "liters": 30.3,
        "cost": 25.2
    }

    AddFillUpRequest.getItemJsonFrom(modelJson)

def test_parseJson_withInvalidJson_deliversError():
    modelJson = {
        "date": "2024-06-29T13:34:30Z",
        "cost": 25.2
    }

    try:
        AddFillUpRequest.getItemJsonFrom(modelJson)
        assert False
    except:
        assert True
    




    