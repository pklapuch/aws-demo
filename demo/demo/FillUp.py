from decimal import Decimal
from .JSONValidationError import JSONValidationError

class FillUp:
    def __init__(self, id, userID, date, kilometers, liters, cost):
        self.id = id
        self.userID = userID
        self.date = date
        self.kilometers = kilometers
        self.liters = liters
        self.cost = cost

    def encodeAsDynamoDbDict(self) -> dict:
        return {
            'id': self.id,
            'userID': self.userID,
            'date': self.date,
            'kilometers': Decimal(str(self.kilometers)),
            'liters': Decimal(str(self.liters)),
            'cost': Decimal(str(self.cost))
        }
    
    def encodeAsJSON(self) -> dict:
        return {
            'id': self.id,
            'userID': self.userID,
            'date': self.date,
            'kilometers': self.kilometers,
            'liters': self.liters,
            'cost': self.cost
        }

    @staticmethod
    def decodeFromJSON(dict):
        try:
            id = dict['id']
            userID = dict['userID']
            date = dict['date']
            kilometers = dict['kilometers']
            liters = dict['liters']
            cost = dict['cost']
            return FillUp(id, userID, date, kilometers, liters, cost)
        except Exception as error:
            raise JSONValidationError(f"Invalidd JSON for FillUp: {error}")   
        
    @staticmethod   
    def decodeFromDynamoDbDict(dict):
        try:
            id = dict['id']
            userID = dict['userID']
            date = dict['date']
            kilometers = FillUp.replace_decimal_with_number(dict['kilometers'])
            liters = FillUp.replace_decimal_with_number(dict['liters'])
            cost = FillUp.replace_decimal_with_number(dict['cost'])
            return FillUp(id, userID, date, kilometers, liters, cost)
        except Exception as error:
            raise JSONValidationError(f"Invalidd DynaamoDB DICT for FillUp: {error}")

    @staticmethod    
    def replace_decimal_with_number(value: Decimal):
        valueStr = str(value)
        return float(valueStr)
    
    def __eq__(self, other): 
        if not isinstance(other, FillUp):
            return False

        if self.id != other.id:
            return False

        if self.userID != other.userID:
            return False
        
        if self.date != other.date:
            return False
        
        if self.kilometers != other.kilometers:
            return False

        if self.liters != other.liters:
            return False

        if self.cost != other.cost:
            return False

        return True
              