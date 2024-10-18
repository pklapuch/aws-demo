import json

class EventResourceHelper:
    @staticmethod
    def loadEventByStringifyingBody(name):
        event = EventResourceHelper.loadEvent(name)
        return EventResourceHelper.mapJsonEventToEventWithStringifiedBody(event)

    @staticmethod
    def mapJsonEventToEventWithStringifiedBody(event):
        newEvent = event
        newEvent["body"] = json.dumps(event["body"])
        return newEvent

    @staticmethod
    def loadEvent(name: str):
        with open(f"events/{name}", 'r') as file:
            return json.load(file)    