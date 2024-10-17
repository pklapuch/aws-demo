from .JSONValidationError import JSONValidationError
from decimal import Decimal

class AddFillUpRequest:
    def __init__(self, date, kilometers, liters, cost):
        self.date = date
        self.kilometers = kilometers
        self.liters = liters
        self.cost = cost

    @staticmethod   
    def decode(json):
        try:
            return AddFillUpRequest(json['date'], json['kilometers'], json['liters'], json['cost'])
        except Exception as error:
            raise JSONValidationError(f"Invalid JSON for AddFillUpRequest: {error}")

    def toDynamoDbInsertDict(self, userID):
        item = {}
        item['userID'] = userID
        item['date'] = self.date
        item ['kilometers'] = Decimal(str(self.kilometers))
        item ['liters'] = Decimal(str(self.liters))
        item ['cost'] = Decimal(str(self.cost))
        return item
    
    def __eq__(self, other): 
        if not isinstance(other, AddFillUpRequest):
            return False

        return self.date == other.date and self.kilometers == other.kilometers and self.liters == other.liters and self.cost == other.cost