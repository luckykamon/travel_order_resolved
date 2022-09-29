from .descriptors import Str, Id, Int, TrainStation
from .train_station import TrainStation as TrainStationDto

class Trip:
    id = Id("id")
    identifier = Str("identifier")
    duration = Int("duration")
    departure_station = TrainStation("departure_station")
    arrival_station = TrainStation("arrival_station")
    
    def __init__(self, id:str=None, identifier:str=None, duration:int=None, departure_station:TrainStationDto=None, arrival_station:TrainStationDto=None):
        self.id = id
        self.identifier = identifier
        self.duration = duration
        self.departure_station = departure_station
        self.arrival_station = arrival_station
        
    def toJson(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "duration": self.duration,
            "departure_station": self.departure_station.toJson(),
            "arrival_station": self.arrival_station.toJson()
        }