import sys
from flask import blueprints, request, jsonify
from .middlewares.result import  resultManager, TypeResult
from .errors.auth_exception import AuthException
from .middlewares.auth import isAuth
from .utils.check_json import check_json, exist_or_raise, exist_or_none

sys.path.append("..")
from services.train_station import TrainStation as TrainStationService 

train_station_request = blueprints.Blueprint('train_station', __name__)

@isAuth
@resultManager(TypeResult.JSON)
@train_station_request.get('/')
def get_train_stations():
    return TrainStationService.getJsonMany()

@isAuth
@resultManager(TypeResult.JSON)
@train_station_request.get('/<id>')
def get_train_station(id):
    return TrainStationService.getJsonOneById(id)

@isAuth
@resultManager(TypeResult.JSON)
@train_station_request.post('/')
def create_train_station():
    create_json = request.json
    
    check_json(create_json)
    
    name = exist_or_raise(create_json, "name")
    slug = exist_or_raise(create_json, "slug")
    address = exist_or_raise(create_json, "address")
    zip_code = exist_or_raise(create_json, "zip_code")
    city = exist_or_raise(create_json, "city")
    country = exist_or_raise(create_json, "country")
    latitude = exist_or_raise(create_json, "latitude")
    longitude = exist_or_raise(create_json, "longitude")

    return TrainStationService.createOne(name, slug, address, zip_code, city, country, latitude, longitude)

@isAuth
@resultManager(TypeResult.JSON)
@train_station_request.put('/<id>')
def update_train_station(id):    
    update_json = request.json
    
    check_json(update_json)
    
    name = exist_or_none(update_json, "name")
    slug = exist_or_none(update_json, "slug")
    address = exist_or_none(update_json, "address")
    zip_code = exist_or_none(update_json, "zip_code")
    city = exist_or_none(update_json, "city")
    country = exist_or_none(update_json, "country")
    latitude = exist_or_none(update_json, "latitude")
    longitude = exist_or_none(update_json, "longitude")
    
    return TrainStationService.updateOne(id, name, slug, address, zip_code, city, country, latitude, longitude)

@isAuth
@resultManager(TypeResult.TEXT)
@train_station_request.delete('/<id>')
def delete_train_station(id):
    return TrainStationService.deleteOne(id)