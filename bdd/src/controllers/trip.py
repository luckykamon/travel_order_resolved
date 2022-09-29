import sys
from flask import blueprints, request, jsonify

sys.path.append("..")
from middlewares.result import resultManager
from middlewares.auth import isAuth
from services.trip import Trip as TripService

trip_request = blueprints.Blueprint('trip', __name__)

@isAuth
@resultManager
@trip_request.get('/')
def get_trips():
    return jsonify(TripService.getJsonMany())

@isAuth
@resultManager
@trip_request.get('/<id>')
def get_trip(id):
    return TripService.getJsonOneById(id)

@isAuth
@resultManager
@trip_request.post('/')
def create_trip():
    return TripService.createOne(request.json)

@isAuth
@resultManager
@trip_request.put('/<id>')
def update_trip(id):
    return TripService.updateOne(id, request.json)

@isAuth
@resultManager
@trip_request.delete('/<id>')
def delete_trip(id):
    return TripService.deleteOne(id)