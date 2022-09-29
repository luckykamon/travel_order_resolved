import sys
from flask import blueprints, request, jsonify

sys.path.append("..")
from middlewares.result import  resultManager
from middlewares.auth import isAuth
from services.train_station import TrainStation as TrainStationService 

train_station_request = blueprints.Blueprint('train_station', __name__)

@isAuth
@resultManager
@train_station_request.get('/')
def get_train_stations():
    return jsonify(TrainStationService.getJsonMany())

@isAuth
@resultManager
@train_station_request.get('/<id>')
def get_train_station(id):
    return TrainStationService.getJsonOneById(id)

@isAuth
@resultManager
@train_station_request.post('/')
def create_train_station():
    return TrainStationService.createOne(request.json)

@isAuth
@resultManager
@train_station_request.put('/<id>')
def update_train_station(id):    
    return TrainStationService.updateOne(id, request.json)

@isAuth
@resultManager
@train_station_request.delete('/<id>')
def delete_train_station(id):
    return TrainStationService.deleteOne(id)