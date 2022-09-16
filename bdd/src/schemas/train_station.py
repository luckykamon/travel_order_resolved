#!/usr/bin/env python3
 
import json
from mongoengine import *

class TrainStation(Document):
    name = StringField(required=True)
    slug = StringField(required=True)
    address = StringField(required=True)
    zip_code = StringField(required=True, min_length=5, max_length=5)
    city = StringField(required=True)
    country = StringField(required=True)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
    
    def __init__(self, name, slug, address, zip_code, city, country, latitude, longitude, *args, **values):
        super().__init__(*args, **values)
        
        self.name = name
        self.slug = slug
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        
    meta = {
        "collection": "train_stations",
        "db_alias": "default"
    }