#!/usr/bin/env python3
 
import json
from mongoengine import *
from .train_station import TrainStation

class Trip(Document):
    identifier = StringField(required=True, unique=True)
    duration = IntField(required=True, min_value=0)
    departure_station = ReferenceField(TrainStation, required=True)
    arrival_station = ReferenceField(TrainStation, required=True)
    
    def __init__(self, identifier, duration, departure_station, arrival_station, *args, **values):
        super().__init__(*args, **values)
        
        self.identifier = identifier
        self.duration = duration
        
        if isinstance(departure_station, str):
            self.departure_station = TrainStation.objects.get(id=departure_station)
        else:
            self.departure_station = departure_station
            
        if isinstance(arrival_station, str):
            self.arrival_station = TrainStation.objects.get(id=arrival_station)
        else:
            self.arrival_station = arrival_station
    
    def to_json(self, *args, **kwargs):      
        super_json = json.loads(super().to_json(*args, **kwargs))
        super_json["departure_station"] = self.departure_station
        super_json["arrival_station"] = self.arrival_station
        return super_json
    
    meta = {
        "collection": "trips",
        "db_alias": "default"
    }