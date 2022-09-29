import sys
from .descriptors import Str, Id, Slug, ZipCode, GpsCoord

sys.path.append("../..")
from schemas.train_station import TrainStation as TrainStationSchema

class TrainStation:
    id = Id("id")
    name = Str("name")
    slug = Slug("slug")
    address = Str("address")
    zip_code = ZipCode("zip_code")
    city = Str("city")
    country = Str("country")
    latitude = GpsCoord("latitude")
    longitude = GpsCoord("longitude")
    
    def __init__(self, id:str=None, name:str=None, slug:str=None, address:str=None, zip_code:str=None, city:str=None, country:str=None, latitude:float=None, longitude:float=None):
        self.id = id
        self.name = name
        self.slug = slug
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        
    def fromDAO(self, train_station:TrainStationSchema):
        self.id = str(train_station.id)
        self.name = train_station.name
        self.slug = train_station.slug
        self.address = train_station.address
        self.zip_code = train_station.zip_code
        self.city = train_station.city
        self.country = train_station.country
        self.latitude = train_station.latitude
        self.longitude = train_station.longitude
        return self
        
    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "address": self.address,
            "zip_code": self.zip_code,
            "city": self.city,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
        