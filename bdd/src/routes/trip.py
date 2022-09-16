#!/usr/bin/env python3

import sys
from flask import blueprints

sys.path.append("..")
from schemas.trip import Trip

trip = blueprints.Blueprint('trip', __name__)

@trip.get('/')
def get_trips():
    return Trip.objects.to_json()

@trip.get('/<id>')
def get_trip(id):
    return Trip.objects.get(id=id).to_json()

@trip.get('/delete/<id>')
def delete_trip(id):
    # delete the train station with the given id
    Trip.objects(id=id).delete()
    return "Trip deleted"

@trip.get('/create')
def create_trip():
    trip = Trip(
        identifier="fgjhkjlmkdzz",
        duration=2,
        departure_station="63247f19d3ce247dbe65d52b",
        arrival_station="63247f1bd3ce247dbe65d52c"
    )
    trip.save()
    
    return trip.to_json()