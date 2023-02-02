import flask
import flask_cors
from graph import index as graph_index
from build import index as build_index
from reformat import index as reformat_index

app = flask.Flask(__name__)
flask_cors.CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/graph', methods=["POST"])
def graph():
    # try:
        if 'Departure' not in flask.request.json or 'Destination' not in flask.request.json:
            raise Exception("No Departure or Destination in json")
        departure = flask.request.json['Departure']
        destination = flask.request.json['Destination']
        timestamp = None
        if 'Timestamp' in flask.request.json:
            timestamp = flask.request.json['Timestamp']
        return (graph_index.index(departure, destination, timestamp), 200)
    # except Exception as e:
    #     return ({"Cannot process" : str(e)}, 500)

@app.route('/build', methods=["GET"])
def build():
    return (build_index.index(), 200)

@app.route('/reformat', methods=["GET"])
def test():
    return (reformat_index.index(), 200)

@app.route('/', methods=["GET"])
def index():
    return("It works graph !", 200)

def main():
    app.run(host="0.0.0.0", port=8000, debug=True)

if __name__ == '__main__':
    main()
