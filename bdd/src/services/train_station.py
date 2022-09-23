import json
import sys
from .crub_interface import CRUBInterface

sys.path.append("..")
from schemas.train_station import TrainStation as TrainStationSchema

class TrainStation(CRUBInterface):
    def getJsonMany():
        return_json = list()
        for train_station in TrainStation.__getMany():
            return_json.append(TrainStation.__getJsonFromObject(train_station))
        return return_json
    
    def getJsonOneById(id):
        return TrainStation.__getJsonFromObject(TrainStation.__getOneById(id))
    
    def __getJsonFromObject(object):
        return json.loads(object.to_json())
    
    def __getMany():
        return TrainStationSchema.objects
    
    def __getOneById(id):
        return TrainStationSchema.objects.get(id=id)
    
    def __ckeckFields(id=None, name=None, slug=None, address=None, zip_code=None, city=None, country=None, latitude=None, longitude=None):
        if (zip_code is not None):
            if (len(zip_code) != 5):
                raise TypeError("Zip code must be 5 characters long")
            if (not zip_code.isdigit()):
                raise TypeError("Zip code must be a number")
        
        if(id is None):
            if (name is not None) and (TrainStationSchema.objects(name=name).count() > 0):
                raise TypeError("Name already exists")
            if (slug is not None) and (TrainStationSchema.objects(slug=slug).count() > 0):
                raise TypeError("Slug already exists")
            if (latitude is not None) and (longitude is not None) and (TrainStationSchema.objects(latitude=latitude, longitude=longitude).count() > 0):
                raise TypeError("A train station already exists at this location")
            if (address is not None) and (zip_code is not None) and (city is not None) and (country is not None) and (TrainStationSchema.objects(address=address, zip_code=zip_code, city=city, country=country).count() > 0):
                raise TypeError("A train station already exists at this address")
        else:
            if (name is not None) and (TrainStationSchema.objects(id__ne=id, name=name).count() > 0):
                raise TypeError("Name already exists")
            if (slug is not None) and (TrainStationSchema.objects(id__ne=id, slug=slug).count() > 0):
                raise TypeError("Slug already exists")
            if (latitude is not None) and (longitude is not None) and (TrainStationSchema.objects(id__ne=id, latitude=latitude, longitude=longitude).count() > 0):
                raise TypeError("A train station already exists at this location")
            if (address is not None) and (zip_code is not None) and (city is not None) and (country is not None) and (TrainStationSchema.objects(id__ne=id, address=address, zip_code=zip_code, city=city, country=country).count() > 0):
                raise TypeError("A train station already exists at this address")

    def createOne(name, slug, address, zip_code, city, country, latitude, longitude):   
        TrainStation.__ckeckFields(name=name, slug=slug, address=address, zip_code=zip_code, city=city, country=country, latitude=latitude, longitude=longitude)
           
        train_station = TrainStationSchema(
            name=name,
            slug=slug,
            address=address,
            zip_code=zip_code,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude
        )
        
        train_station.save()
        return TrainStation.__getJsonFromObject(train_station)
    
    def updateOne(id, name=None, slug=None, address=None, zip_code=None, city=None, country=None, latitude=None, longitude=None):
        train_station = TrainStation.__getOneById(id)
        
        TrainStation.__ckeckFields(id, name=name, slug=slug, address=address, zip_code=zip_code, city=city, country=country, latitude=latitude, longitude=longitude)
        
        if name is not None:
            train_station.update(name=name)
        if slug is not None:
            train_station.update(slug=slug)
        if address is not None:
            train_station.update(address=address)
        if zip_code is not None:
            train_station.update(zip_code=zip_code)
        if city is not None:
            train_station.update(city=city)
        if country is not None:
            train_station.update(country=country)
        if latitude is not None:
            train_station.update(latitude=latitude)
        if longitude is not None:
            train_station.update(longitude=longitude)
        
        train_station.reload()
        return TrainStation.__getJsonFromObject(train_station)
    
    def deleteOne(id):
        train_station = TrainStation.__getOneById(id)
        train_station.delete()
        
        return "Train station deleted"
        