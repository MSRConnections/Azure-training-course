import json

# this class contains a longitude, latitude and temperature
class MsrPayload:
    def __init__(self, lng, lat, temp):
        #add location details and some extra data here
        self.lng = lng
        self.lat = lat
        self.temp = temp

    def GetJSONObject(self):
        return json.dumps(self.__dict__)
