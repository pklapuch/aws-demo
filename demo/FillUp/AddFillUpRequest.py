from demo.FillUp.JSONValidationError import JSONValidationError
from decimal import Decimal

class AddFillUpRequest:
    def __init__(self, date, kilometers, liters, cost):
        self.date = date
        self.kilometers = kilometers
        self.liters = liters
        self.cost = cost

    def test(self):
        print("")

    @staticmethod
    def getItemJsonFrom(json):
        item = {}

        try:
            item['date'] = json['date']
        except:
            raise JSONValidationError("`date` not set!")
    
        try:
            item['kilometers'] = Decimal(str(json['kilometers']))
        except:
            raise JSONValidationError("`kilometers` not set!")
        
        try:
            item['liters'] = Decimal(str(json['liters']))
        except:
            raise JSONValidationError("`liters` not set!")
        
        try:
            item['cost'] = Decimal(str(json['cost']))
        except:
            raise JSONValidationError("`cost` not set!")        
        
        return item