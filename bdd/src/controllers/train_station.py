import sys
from flask import blueprints, request

sys.path.append("..")
from middlewares.auth import isAuth
from middlewares.result import resultManager, ResultManagerType
from services.train_station import TrainStation as TrainStationService 

train_station_request = blueprints.Blueprint('train_station', __name__)

@train_station_request.get('/')
@isAuth
@resultManager(ResultManagerType.JSON)
def get_train_stations():
    return TrainStationService.getJsonMany()

@train_station_request.get('/<id>')
@isAuth
@resultManager(ResultManagerType.JSON)
def get_train_station(id):
    return TrainStationService.getJsonOneById(id)

@train_station_request.post('/')
@isAuth
@resultManager(ResultManagerType.JSON)
def create_train_station():
    return TrainStationService.createOne(request.json)

@train_station_request.put('/<id>')
@isAuth
@resultManager(ResultManagerType.JSON)
def update_train_station(id):    
    return TrainStationService.updateOne(id, request.json)

@train_station_request.delete('/<id>')
@isAuth
@resultManager(ResultManagerType.TEXT)
def delete_train_station(id):
    return TrainStationService.deleteOne(id)