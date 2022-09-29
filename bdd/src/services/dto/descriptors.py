from bson import ObjectId
from .train_station import TrainStation as TrainStationDto

class BaseDescriptor(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

class Str(BaseDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} : must be a string")
        instance.__dict__[self.name] = value
        
class Id(Str):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} : must be a string")
        if not ObjectId.is_valid(value):
            raise TypeError(f"{self.name} : must be a valid ObjectId")
        instance.__dict__[self.name] = value
        
class Slug(Str):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} : must be a string")
        if " " in value:
            raise TypeError(f"{self.name} : must not contain spaces")
        if "-" in value:
            raise TypeError(f"{self.name} : must not contain dashes")
        if "." in value:
            raise TypeError(f"{self.name} : must not contain dots")
        if not value.islower():
            raise TypeError(f"{self.name} : must be lowercase")
        
        instance.__dict__[self.name] = value
        
class ZipCode(Str):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} : must be a string")
        if (len(value) != 5):
            raise TypeError(f"{self.name} : must be 5 characters long")
        if (not value.isnumeric()):
            raise TypeError(f"{self.name} : must be a number")
        
        instance.__dict__[self.name] = value
        
class Int(BaseDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except:
                raise TypeError(f"{self.name} : must be an integer")
        
        instance.__dict__[self.name] = value
        
class GpsCoord(BaseDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, float):
            try:
                value = float(value)
            except:
                raise TypeError(f"{self.name} : must be a float")
        
        instance.__dict__[self.name] = value
        
class Uuid(BaseDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} : must be a string")
        if len(value) != 36:
            raise TypeError(f"{self.name} : must be 36 characters long")
        if value[8] != "-" or value[13] != "-" or value[18] != "-" or value[23] != "-":
            raise TypeError(f"{self.name} : must contain 4 dashes")
        
        instance.__dict__[self.name] = value

class TrainStation(BaseDescriptor):
    def __set__(self, instance, value):
        if not isinstance(value, TrainStationDto):
            raise TypeError(f"{self.name} : must be a TrainStation")
        instance.__dict__[self.name] = value