import sys
from flask import blueprints, request, jsonify

sys.path.append("..")
from services.train_station import TrainStation as TrainStationService 
from middlewares.auth_api_token import auth_token
from errors.auth_exception import AuthException

train_station_request = blueprints.Blueprint('train_station', __name__)

@train_station_request.get('/')
def get_train_stations():
    try:
        auth_token(request.headers.get('api_key'))
        return jsonify(TrainStationService.getJsonMany()), 200
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400

@train_station_request.get('/<id>')
def get_train_station(id):
    try:
        auth_token(request.headers.get('api_key'))
        return jsonify(TrainStationService.getJsonOneById(id)), 200
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400

@train_station_request.post('/')
def create_train_station():
    try:
        auth_token(request.headers.get('api_key'))
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400
    
    create_json = request.json
    if create_json is None:
        return "No JSON found", 400
    if ("name" not in create_json.keys()) or ("slug" not in create_json.keys()) or ("address" not in create_json.keys()) or ("zip_code" not in create_json.keys()) or ("city" not in create_json.keys()) or ("country" not in create_json.keys()) or ("latitude" not in create_json.keys()) or ("longitude" not in create_json.keys()):
        return "Missing fields", 400
    
    try:
        return jsonify(TrainStationService.createOne(create_json["name"], create_json["slug"], create_json["address"], create_json["zip_code"], create_json["city"], create_json["country"], create_json["latitude"], create_json["longitude"])), 201
    except Exception as e:
        return str(e), 400

@train_station_request.put('/<id>')
def update_train_station(id):
    try:
        auth_token(request.headers.get('api_key'))
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400
    
    update_json = request.json
    if update_json is None:
        return "No JSON found", 400
    
    name = update_json["name"] if "name" in update_json.keys() else None
    slug = update_json["slug"] if "slug" in update_json.keys() else None
    address = update_json["address"] if "address" in update_json.keys() else None
    zip_code = update_json["zip_code"] if "zip_code" in update_json.keys() else None
    city = update_json["city"] if "city" in update_json.keys() else None
    country = update_json["country"] if "country" in update_json.keys() else None
    latitude = update_json["latitude"] if "latitude" in update_json.keys() else None
    longitude = update_json["longitude"] if "longitude" in update_json.keys() else None
    
    try:
        return jsonify(TrainStationService.updateOne(id, name, slug, address, zip_code, city, country, latitude, longitude)), 200
    except Exception as e:
        return str(e), 400

@train_station_request.delete('/<id>')
def delete_train_station(id):
    try:
        auth_token(request.headers.get('api_key'))
        return TrainStationService.deleteOne(id), 200
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400