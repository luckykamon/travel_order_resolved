import sys
import json
from .crub_interface import CRUBInterface

sys.path.append("..")
from schemas.train_station import TrainStation as TrainStationSchema
from dto.train_station import TrainStation as TrainStationDTO
    
class TrainStation(CRUBInterface):
    # GET 
    def __getJsonFromDao(dao:TrainStationSchema):        
        return TrainStationDTO(dao=dao).toJson()
    
    def __getMany():
        return TrainStationSchema.objects
    
    def getJsonMany():
        return_json = list()
        for dao in TrainStation.__getMany():
            return_json.append(TrainStation.__getJsonFromDao(dao))
        return return_json
    
    def getOneById(id):
        return TrainStationSchema.objects.get(id=id)
    
    def __getOneById(id):
        return TrainStationSchema.objects.get(id=id)
    
    def getJsonOneById(id):
        return TrainStation.__getJsonFromDao(TrainStation.__getOneById(id))
    
    # CHECK
    def __ckeckFields(dto:TrainStationDTO):
        if TrainStation.__trainStationNameAlreadyExist(dto):
            raise TypeError("Name already exists")
        if TrainStation.__trainStationSlugAlreadyExist(dto):
            raise TypeError("Slug already exists")
        if TrainStation.__trainStationGpsAlreadyExist(dto):
            raise TypeError("A train station already exists at this location")
        if TrainStation.__trainStationAddressAlreadyExist(dto):
            raise TypeError("A train station already exists at this address")

    def __trainStationNameAlreadyExist(dto:TrainStationDTO):
        if dto.name is None:
            return False
        if dto.id is None:
            return TrainStationSchema.objects(name=dto.name).count() > 0
        return TrainStationSchema.objects(id__ne=dto.id, name=dto.name).count() > 0
    
    def __trainStationSlugAlreadyExist(dto:TrainStationDTO):
        if dto.name is None:
            return False
        if dto.id is None:
            return TrainStationSchema.objects(slug=dto.slug).count() > 0
        return TrainStationSchema.objects(id__ne=dto.id, slug=dto.slug).count() > 0

    def __trainStationGpsAlreadyExist(dto:TrainStationDTO):
        if (dto.latitude is None) or (dto.longitude is None):
            return False
        if dto.id is None:
            return TrainStationSchema.objects(latitude=dto.latitude, longitude=dto.longitude).count() > 0
        return TrainStationSchema.objects(id__ne=dto.id, latitude=dto.latitude, longitude=dto.longitude).count() > 0
    
    def __trainStationAddressAlreadyExist(dto:TrainStationDTO):
        if (dto.address is None) or (dto.zip_code is None) or (dto.city is None) or (dto.country is None):
            return False
        if dto.id is None:
            return TrainStationSchema.objects(address=dto.address, zip_code=dto.zip_code, city=dto.city, country=dto.country).count() > 0
        return TrainStationSchema.objects(id__ne=dto.id, address=dto.address, zip_code=dto.zip_code, city=dto.city, country=dto.country).count() > 0

    # CREATE
    def createOne(json:dict):   
        dto = TrainStationDTO(json=json)
        dto.id = None
        
        TrainStation.__ckeckFields(dto)
                  
        train_station = dto.toDao()
        train_station.save()
        
        return TrainStation.__getJsonFromDao(train_station)
    
    # UPDATE
    def updateOne(id, json:dict):
        train_station = TrainStation.__getOneById(id)
    
        dto = TrainStationDTO(dao=train_station)
        
        update_keys = ["name", "slug", "address", "zip_code", "city", "country", "latitude", "longitude"]
        for key, value in json.items():
            if (value is not None) and (key in update_keys):
                setattr(dto, key, value)                
    
        TrainStation.__ckeckFields(dto)
        
        train_station = dto.toDao()
        train_station.save()
        
        return TrainStation.__getJsonFromDao(train_station)
    
    # DELETE
    def deleteOne(id):
        train_station = TrainStation.__getOneById(id)
        train_station.delete()
        
        return "Train station deleted"