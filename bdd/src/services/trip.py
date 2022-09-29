import sys
import json
from .crub_interface import CRUBInterface
from .train_station import TrainStation as TrainStationService

sys.path.append("..")
from schemas.trip import Trip as TripSchema
from dto.trip import Trip as TripDTO

class Trip(CRUBInterface):
    # GET
    def __getJsonFromDao(dao:TripSchema):      
        trip = TripDTO()
        trip.fromDao(dao)
        return_json = trip.toJson()
        return_json["departure_station"] = TrainStationService.getJsonOneById(trip.departure_station)
        return_json["arrival_station"] = TrainStationService.getJsonOneById(trip.arrival_station)
        return return_json
    
    def __getMany():
        return TripSchema.objects
    
    def getJsonMany():
        return_json = list()
        for trip in Trip.__getMany():
            return_json.append(Trip.__getJsonFromDao(trip))
        return json.dumps(return_json)
    
    def __getOneById(id):
        return TripSchema.objects.get(id=id)
    
    def getJsonOneById(id):
        return Trip.__getJsonFromDao(Trip.__getOneById(id))
    
    # CHECK
    def __ckeckFields(dto:TripDTO):
        if Trip.__tripTrainStationsIsSame(dto):
            raise TypeError("Departure and arrival stations must be different")
        if Trip.__tripDurationIsNegative(dto):
            raise TypeError("Duration must be positive")
        if Trip.__tripIdentifierExists(dto):
            raise TypeError("Identifier already exists")
        if Trip.__tripExists(dto):
            raise TypeError("A trip already exists between these stations")
    
    def __tripTrainStationsIsSame(dto:TripDTO):
        return (dto.departure_station is not None) and (dto.arrival_station is not None) and (dto.departure_station == dto.arrival_station)

    def __tripDurationIsNegative(dto:TripDTO):
        return (dto.duration is not None) and (dto.duration < 0)
    
    def __tripIdentifierExists(dto:TripDTO):
        if dto.identifier is None:
            return False
        if dto.id is None:
            return TripSchema.objects(identifier=dto.identifier).count() > 0
        return TripSchema.objects(id__ne=dto.id, identifier=dto.identifier).count() > 0
    
    def __tripExists(dto:TripDTO):
        if (dto.departure_station is None) or (dto.arrival_station is None):
            return False
        if dto.id is None:
            return TripSchema.objects(departure_station=dto.departure_station, arrival_station=dto.arrival_station).count() > 0
        return TripSchema.objects(id__ne=dto.id, departure_station=dto.departure_station, arrival_station=dto.arrival_station).count() > 0
    
    # CREATE
    def create(json):
        dto = TripDTO()
        dto.fromJson(json)
        dto.id = None
        
        Trip.__ckeckFields(dto)
        
        trip = dto.toDao()
        trip.save()
    
        return Trip.__getJsonFromDao(trip)
    
    # UPDATE
    def update(id, json):
        dto = TripDTO()
        dto.fromJson(json)
        dto.id = id
        
        Trip.__ckeckFields(dto)
        
        trip = Trip.__getOneById(id)
        
        update_keys = ["duration"]
        for key, value in dto.toJson().items():
            if (value is not None) and (key in update_keys):
                trip.update(**{key: value})
                
        trip.reload()
        return Trip.__getJsonFromDao(trip)
    
    # DELETE
    def delete(id):
        trip = Trip.__getOneById(id)
        trip.delete()
        
        return "Trip deleted"