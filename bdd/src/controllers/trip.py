import sys
from flask import blueprints, request

sys.path.append("..")
from middlewares.auth import isAuth
from middlewares.result import resultManager, ResultManagerType
from services.trip import Trip as TripService

trip_request = blueprints.Blueprint('trip', __name__)

@trip_request.get('/')
@isAuth
@resultManager(ResultManagerType.JSON)
def get_trips():
    return TripService.getJsonMany()

@trip_request.get('/<id>')
@isAuth
@resultManager(ResultManagerType.JSON)
def get_trip(id):
    return TripService.getJsonOneById(id)

@trip_request.post('/')
@isAuth
@resultManager(ResultManagerType.JSON)
def create_trip():
    return TripService.createOne(request.json)

@trip_request.put('/<id>')
@isAuth
@resultManager(ResultManagerType.JSON)
def update_trip(id):
    return TripService.updateOne(id, request.json)

@trip_request.delete('/<id>')
@isAuth
@resultManager(ResultManagerType.TEXT)
def delete_trip(id):
    return TripService.deleteOne(id)