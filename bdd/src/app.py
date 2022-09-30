import os
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from controllers.trip import trip_request
from controllers.train_station import train_station_request

is_dev_env = os.environ.get('ENV_VAR') == 'dev'

db = MongoEngine()
app = Flask(__name__)
CORS(app)
app.config["MONGODB_SETTINGS"] = [
   {
      "db": os.environ.get('DB_NAME'),
      "host": os.environ.get('DB_HOST'),
      "port": int(os.environ.get('DB_PORT')),
      "alias": "default",
      "username": os.environ.get('DB_USER'),
      "password": os.environ.get('DB_PASSWORD')
   }
]
db.init_app(app)

app.register_blueprint(trip_request, url_prefix='/trip')
app.register_blueprint(train_station_request, url_prefix='/train_station')
 
@app.route('/')
def welcome():
   return "Welcome to the API"
 
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=3000, debug=is_dev_env)