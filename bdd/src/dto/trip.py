import sys
from bson import ObjectId
from .utils.check_type import check_id, check_int, check_str
from .utils.check_json import get_key, check_json
from .dto_interface import DtoInterface
from .train_station import TrainStation as TrainStationDto

sys.path.append("..")
from schemas.trip import Trip as TripSchema

class Trip(DtoInterface):    
    def __init__(self, json=None, dao=None):
        if (json is not None) and (dao is not None):
            raise ValueError("Only one parameter is required (json or dao)")
        if (json is None) and (dao is None):
            raise ValueError("One parameter is required (json or dao)")
        
        if json is not None:
            self.__fromJson(json)
        if dao is not None:
            self.__fromDao(dao)
            
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
            "id": str(self.id),
            "identifier": self.identifier,
            "duration": self.duration,
            "departure_station": str(self.departure_station),
            "arrival_station": str(self.arrival_station)
        }
        
    def __fromJson(self, json):
        check_json(json)
        
        self.id = get_key(json, "id")
        self.identifier = get_key(json, "identifier")
        self.duration = get_key(json, "duration")
        self.departure_station = get_key(json, "departure_station")
        self.arrival_station = get_key(json, "arrival_station")
        
    def toDao(self):
        trip = TripSchema()
        
        if self.id is not None:
            trip.id = str(self.id)
            
        trip.identifier = self.identifier
        trip.duration = self.duration
        trip.departure_station = self.departure_station
        trip.arrival_station = self.arrival_station
        
        return trip
        
    def __fromDao(self, dao:TripSchema):
        self.id = str(dao.id)
        self.identifier = dao.identifier
        self.duration = dao.duration
        self.departure_station = str(dao.departure_station if isinstance(dao.departure_station, ObjectId) else dao.departure_station.id)
        self.arrival_station = str(dao.arrival_station if isinstance(dao.arrival_station, ObjectId) else dao.arrival_station.id)