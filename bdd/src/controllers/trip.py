import sys
from flask import blueprints, request, jsonify
from .middlewares.auth import isAuth
from .errors.auth_exception import AuthException
from .middlewares.result import resultManager, TypeResult
from .utils.check_json import check_json, exist_or_raise, exist_or_none

sys.path.append("..")
from services.trip import Trip as TripService

trip_request = blueprints.Blueprint('trip', __name__)

@isAuth
@resultManager(TypeResult.JSON)
@trip_request.get('/')
def get_trips():
    return TripService.getJsonMany()

@isAuth
@resultManager(TypeResult.JSON)
@trip_request.get('/<id>')
def get_trip(id):
    return TripService.getJsonOneById(id)

@isAuth
@resultManager(TypeResult.JSON)
@trip_request.post('/')
def create_trip():
    create_json = request.json  
    
    check_json(create_json)
    
    identifier = exist_or_raise(create_json, "identifier")
    duration = exist_or_raise(create_json, "duration")
    departure_station = exist_or_raise(create_json, "departure_station")
    arrival_station = exist_or_raise(create_json, "arrival_station")
    
    return TripService.createOne(identifier, duration, departure_station, arrival_station)

@isAuth
@resultManager(TypeResult.JSON)
@trip_request.put('/<id>')
def update_trip(id):
    update_json = request.json
    
    check_json(update_json)
    
    duration = exist_or_none(update_json, "duration")
    
    return TripService.updateOne(id, duration)

@isAuth
@resultManager(TypeResult.TEXT)
@trip_request.delete('/<id>')
def delete_trip(id):
    return TripService.deleteOne(id)