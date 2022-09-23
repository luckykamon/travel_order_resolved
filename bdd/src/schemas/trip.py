import json
from mongoengine import Document, StringField, IntField, ReferenceField
from .train_station import TrainStation

class Trip(Document):
    identifier = StringField(required=True, unique=True)
    duration = IntField(required=True, min_value=0)
    departure_station = ReferenceField(TrainStation, required=True)
    arrival_station = ReferenceField(TrainStation, required=True)
    
    meta = {
        "collection": "trips",
        "db_alias": "default"
    }