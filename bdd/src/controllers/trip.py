import sys
from flask import blueprints, request, jsonify

sys.path.append("..")
from services.trip import Trip as TripService
from middlewares.auth_api_token import auth_token
from errors.auth_exception import AuthException

trip_request = blueprints.Blueprint('trip', __name__)

@trip_request.get('/')
def get_trips():
    try:
        auth_token(request.headers.get('api_key'))
        return jsonify(TripService.getJsonMany()), 200
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400

@trip_request.get('/<id>')
def get_trip(id):
    try:
        auth_token(request.headers.get('api_key'))
        return jsonify(TripService.getJsonOneById(id)), 200
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400

@trip_request.post('/')
def create_trip():
    try:
        auth_token(request.headers.get('api_key'))
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400
    
    create_json = request.json  
    if create_json is None:
        return "No JSON found", 400
    if ("identifier" not in create_json.keys()) or ("duration" not in create_json.keys()) or ("departure_station" not in create_json.keys()) or ("arrival_station" not in create_json.keys()):
        return "Missing fields", 400
    
    try:
        return jsonify(TripService.createOne(create_json["identifier"], create_json["duration"], create_json["departure_station"], create_json["arrival_station"])), 201
    except Exception as e:
        return str(e), 400

@trip_request.put('/<id>')
def update_trip(id):
    try:
        auth_token(request.headers.get('api_key'))
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400
    
    update_json = request.json
    if update_json is None:
        return "No JSON found", 400
    
    duration = update_json["duration"] if "duration" in update_json.keys() else None
    
    try:
        return jsonify(TripService.updateOne(id, duration)), 200
    except Exception as e:
        return str(e), 400

@trip_request.delete('/<id>')
def delete_trip(id):
    try:
        auth_token(request.headers.get('api_key'))
        return TripService.deleteOne(id), 200
    except AuthException as e:
        return str(e), 401
    except Exception as e:
        return str(e), 400