import sys
from .utils.check_type import check_id, check_str, check_slug, check_zip_code, check_float
from .utils.check_json import exist_in_json_or_raise

sys.path.append("../..")
from schemas.train_station import TrainStation as TrainStationSchema

class TrainStation:    
    def __init__(self):
        pass
        
    @property
    def id(self):
        return self._id
        
    @id.setter
    def id(self, value):
        self._id = check_id("id", value)
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, value):
        self._name = check_str("name", value)
        
    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, value):
        self._slug = check_slug("slug", value)
        
    @property
    def address(self):
        return self._address
        
    @address.setter
    def address(self, value):
        self._address = check_str("address", value)
        
    @property
    def zip_code(self):
        return self._zip_code
        
    @zip_code.setter
    def zip_code(self, value):
        self._zip_code = check_zip_code("zip_code", value)
        
    @property
    def city(self):
        return self._city
        
    @city.setter
    def city(self, value):
        self._city = check_str("city", value)
        
    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value):
        self._country = check_str("country", value)
        
    @property
    def latitude(self):
        return self._latitude
        
    @latitude.setter
    def latitude(self, value):
        self._latitude = check_float("latitude", value)
        
    @property
    def longitude(self):
        return self._longitude
        
    @longitude.setter
    def longitude(self, value):
        self._longitude = check_float("longitude", value)
        
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
        
    def fromJson(self, json):
        self.id = exist_in_json_or_raise(json, "id")
        self.name = exist_in_json_or_raise(json, "name")
        self.slug = exist_in_json_or_raise(json, "slug")
        self.address = exist_in_json_or_raise(json, "address")
        self.zip_code = exist_in_json_or_raise(json, "zip_code")
        self.city = exist_in_json_or_raise(json, "city")
        self.country = exist_in_json_or_raise(json, "country")
        self.latitude = exist_in_json_or_raise(json, "latitude")
        self.longitude = exist_in_json_or_raise(json, "longitude")
        
    def toDao(self):
        train_station = TrainStationSchema()
        for key, value in self.toJson().items():
            if value is not None:
                setattr(train_station, key, value)
        return train_station
        
    def fromDao(self, dao):     
        self.id = str(dao.id)
        self.name = dao.name
        self.slug = dao.slug
        self.address = dao.address
        self.zip_code = dao.zip_code
        self.city = dao.city
        self.country = dao.country
        self.latitude = dao.latitude
        self.longitude = dao.longitude
        