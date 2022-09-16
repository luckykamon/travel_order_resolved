#!/usr/bin/env python3

import sys
from flask import blueprints

sys.path.append("..")
from schemas.train_station import TrainStation

train_station = blueprints.Blueprint('train_station', __name__)

@train_station.get('/')
def get_train_stations():
    return TrainStation.objects().to_json()

@train_station.get('/<id>')
def get_train_station(id):
    return TrainStation.objects.get(id=id).to_json()

@train_station.get('/create')
def create_train_station():
    train_station = TrainStation(
        name="Gare de Lyon",
        slug="gare-de-lyon",
        address="1 Rue de Lyon, 75012 Paris",
        zip_code="75012",
        city="Paris",
        country="France",
        latitude=48.844444,
        longitude=2.374444
    )
    train_station.save()
    
    return train_station.to_json()