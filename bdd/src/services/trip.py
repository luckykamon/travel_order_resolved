import json
import sys
from .crub_interface import CRUBInterface

sys.path.append("..")
from schemas.trip import Trip as TripSchema
from .train_station import TrainStation as TrainStationService

class Trip(CRUBInterface):
    def getJsonMany():
        return_json = []
        for trip in Trip.__getMany():
            return_json.append(Trip.__getJsonFromObject(trip))
        return return_json
    
    def getJsonOneById(id):
        return Trip.__getJsonFromObject(Trip.__getOneById(id))
    
    def __getJsonFromObject(object):
        return_json = json.loads(object.to_json())
        return_json["departure_station"] = json.loads(TrainStationService.getJsonOneById(return_json["departure_station"]["$oid"]))
        return_json["arrival_station"] = json.loads(TrainStationService.getJsonOneById(return_json["arrival_station"]["$oid"]))
        return return_json
    
    def __getMany():
        return TripSchema.objects
    
    def __getOneById(id):
        return TripSchema.objects.get(id=id)
    
    def __ckeckFields(id=None, identifier=None, duration=None, departure_station=None, arrival_station=None):
        if (departure_station is not None) and (arrival_station is not None) and (departure_station == arrival_station):
            raise TypeError("Departure and arrival stations must be different")
        if (duration is not None) and (duration < 0):
            raise TypeError("Duration must be positive")
        
        if id is None:
            if (identifier is not None) and TripSchema.objects(identifier=identifier).count() > 0:
                raise TypeError("Identifier already exists") 
            if (departure_station is not None) and (arrival_station is not None) and TripSchema.objects(departure_station=departure_station, arrival_station=arrival_station).count() > 0:
                raise TypeError("A trip already exists between these stations")
        else:
            if (identifier is not None) and TripSchema.objects(id__ne=id, identifier=identifier).count() > 0:
                raise TypeError("Identifier already exists") 
            if (departure_station is not None) and (arrival_station is not None) and TripSchema.objects(id__ne=id, departure_station=departure_station, arrival_station=arrival_station).count() > 0:
                raise TypeError("A trip already exists between these stations")

    def createOne(identifier, duration, departure_station, arrival_station):
        Trip.__ckeckFields(identifier=identifier, duration=duration, departure_station=departure_station, arrival_station=arrival_station)
        
        trip = TripSchema(
            identifier=identifier,
            duration=duration,
            departure_station=departure_station,
            arrival_station=arrival_station
        )
        
        trip.save()
        return Trip.__getJsonFromObject(trip)
    
    def updateOne(id, duration=None):
        trip = Trip.__getOneById(id)
        
        Trip.__ckeckFields(id=id, duration=duration)
        
        if duration is not None:
            trip.update(duration=duration)
            
        trip.reload()
        return Trip.__getJsonFromObject(trip)
    
    def deleteOne(id):
        trip = Trip.__getOneById(id)
        trip.delete()
        
        return "Trip deleted"