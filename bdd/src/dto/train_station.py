import sys
from .utils.check_type import check_id, check_str, check_slug, check_zip_code, check_float
from .utils.check_json import check_json, get_key
from .dto_interface import DtoInterface

sys.path.append("../..")
from schemas.train_station import TrainStation as TrainStationSchema

class TrainStation(DtoInterface):    
    def __init__(self, json=None, dao=None):
        if (json is not None) and (dao is not None):
            raise ValueError("Only one parameter is required (json or dao)")
        if (json is None) and (dao is None):
            raise ValueError("One parameter is required (json or dao)")
        
        if json is not None:
            self.__fromJson(json)
        if dao is not None:
            self.__fromDao(dao)
        
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
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "address": self.address,
            "zip_code": self.zip_code,
            "city": self.city,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
        
    def __fromJson(self, json):
        check_json(json)
        
        self.id = get_key(json, "id")
        self.name = get_key(json, "name")
        self.slug = get_key(json, "slug")
        self.address = get_key(json, "address")
        self.zip_code = get_key(json, "zip_code")
        self.city = get_key(json, "city")
        self.country = get_key(json, "country")
        self.latitude = get_key(json, "latitude")
        self.longitude = get_key(json, "longitude")
        
    def toDao(self):
        train_station = TrainStationSchema()
        
        if self.id is not None:
            train_station.id = self.id
        
        train_station.name = self.name
        train_station.slug = self.slug
        train_station.address = self.address
        train_station.zip_code = self.zip_code
        train_station.city = self.city
        train_station.country = self.country
        train_station.latitude = self.latitude
        train_station.longitude = self.longitude

        return train_station
        
    def __fromDao(self, dao):  
        self.id = str(dao.id)
        self.name = dao.name
        self.slug = dao.slug
        self.address = dao.address
        self.zip_code = dao.zip_code
        self.city = dao.city
        self.country = dao.country
        self.latitude = dao.latitude
        self.longitude = dao.longitude
        