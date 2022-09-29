import sys
from .utils.check_type import check_id, check_int, check_str
from .utils.check_json import exist_in_json_or_raise

sys.path.append("..")
from schemas.trip import Trip as TripSchema

class Trip:    
    def __init__(self):
        pass
        
    @property
    def id(self):
        return self._id
        
    @id.setter
    def id(self, value):
        self._id = check_id("id", value)
        
    @property
    def identifier(self):
        return self._identifier
        
    @identifier.setter
    def identifier(self, value):
        self._identifier = check_str("identifier", value)
        
    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = check_int("duration", value)
        
    @property
    def departure_station(self):
        return self._departure_station
        
    @departure_station.setter
    def departure_station(self, value):
        self._departure_station = check_id("departure_station", value)
        
    @property
    def arrival_station(self):
        return self._arrival_station
        
    @arrival_station.setter
    def arrival_station(self, value):
        self._arrival_station = check_id("arrival_station", value)
        
    def toJson(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "duration": self.duration,
            "departure_station": self.departure_station,
            "arrival_station": self.arrival_station
        }
        
    def fromJson(self, json):
        self.id = exist_in_json_or_raise(json, "id")
        self.identifier = exist_in_json_or_raise(json, "identifier")
        self.duration = exist_in_json_or_raise(json, "duration")
        self.departure_station = exist_in_json_or_raise(json, "departure_station")
        self.arrival_station = exist_in_json_or_raise(json, "arrival_station")
        
    def toDao(self):
        trip = TripSchema()
        for key, value in self.toJson().items():
            if value is not None:
                setattr(trip, key, value)
        return trip
        
    def fromDao(self, dao):
        self.id = str(dao.id)
        self.identifier = dao.identifier
        self.duration = dao.duration
        self.departure_station = dao.departure_station
        self.arrival_station = dao.arrival_station
        