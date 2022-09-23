from mongoengine import Document, StringField, FloatField

class TrainStation(Document):
    name = StringField(required=True, unique=True)
    slug = StringField(required=True, unique=True)
    address = StringField(required=True)
    zip_code = StringField(required=True, min_length=5, max_length=5)
    city = StringField(required=True)
    country = StringField(required=True)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
        
    meta = {
        "collection": "train_stations",
        "db_alias": "default"
    }