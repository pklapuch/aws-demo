import json

class EventResourceHelper:
    @staticmethod
    def loadEventByStringifyingBody(name):
        event = EventResourceHelper.loadEvent(name)
        return EventResourceHelper.mapJsonEventToEventWithStringifiedBody(event)

    def insertUserIdentity(event: dict, userID: str):
        newEvent = event
        newEvent["requestContext"]["authorizer"]["claims"]["sub"] = userID
        return newEvent

    @staticmethod
    def mapJsonEventToEventWithStringifiedBody(event):
        body: str = None

        try:
            body = event["body"]
        except:
            return event

        newEvent = event
        newEvent["body"] = json.dumps(body)
        return newEvent

    @staticmethod
    def loadEvent(name: str):
        with open(f"events/{name}", 'r') as file:
            return json.load(file)    