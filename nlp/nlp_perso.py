import flask
# import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import re
import flask_cors
# import requests

app = flask.Flask(__name__)
flask_cors.CORS(app, resources={r'/*': {'origins': '*'}})

def getLines(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip().lower() for line in lines]
    return lines

def get_result(list_data, depuis, cities):
    gares = []
    for i in list_data:
        if i.lower() in cities:
            gares.append(i)
    if len(gares) != 2:
        return gares
    for i in depuis:
        if i in list_data:
            if list_data[list_data.index(i) + 1] == gares[0] or \
            (list_data.index(i) + 2 < len(list_data) and list_data[list_data.index(i) + 2] == gares[0]):
                return gares
            gares.reverse()
            return(gares)
    return(gares)

def may_reverse(data, depuis, gares):
    for i in depuis:
        if i in data:
            idx = data.find(i)
            if idx > data.find(gares[0].lower()) and idx < data.find(gares[1].lower()):
                gares.reverse()
    return(gares)

def tokenized(data,filtre_stopfr, sp_pattern):
    d = " ".join(str(x) for x in sp_pattern(data))
    return (filtre_stopfr(word_tokenize(d, language="french")))

def check_whole_word(city, data, idx):
    if (idx == 0):
        if (len(city) + idx < len(data)):
            if (not data[idx + len(city)].isalnum()):
                return(True)
            return(False)
        return(False)
    if (len(city) + idx < len(data)):
        if ((not data[idx + len(city)].isalnum()) and (not data[idx - 1].isalnum())):
            return(True)
        return(False)
    if (len(city) + idx == len(data)):
        return(True)
    return(False)

@app.route("/trip", methods=["POST"])
def trip():
    try:
        if not 'data' in flask.request.json:
            raise Exception("No data in json")
        data = flask.request.json['data'].lower()
        gares = []
        cities = getLines("all_gares.txt")
        for city in cities:
            if data.find(city) != -1:
                idx = data.find(city)
                if (check_whole_word(city, data, idx)):
                    gares.append(city.title())
        # data = flask.request.json['data']
        # french_stopwords = set(stopwords.words('french'))
        # filtre_stopfr =  lambda text: [token for token in text if token not in french_stopwords]
        # sp_pattern = re.compile("""[\.\!\"\s\?\-\,\']+""", re.M).split
        # list_d = tokenized(data, filtre_stopfr, sp_pattern)
        # list_d = [value for value in list_d if value != "/"]
        # list_d = mergeCityName(list_d)
        # print(list_d)
        # cities = getLines("all_gares.txt")
        # depuis = getLines("depuis.txt")
        # gares = get_result(list_d, depuis, cities)
        if len(gares) != 2:
            return ({f"Not exactly 2 station given" : gares}, 400)
        print(f"data.find(gares[1]) = {data.find(gares[1].lower())} and data.find(gares[0]) = {data.find(gares[0].lower())}")
        if data.find(gares[1].lower()) < data.find(gares[0].lower()):
            gares.reverse()
        depuis = getLines("depuis.txt")
        gares = may_reverse(data, depuis, gares)
        return ({"Departure": gares[0], "Destination": gares[1]})
    except Exception as e:
        return ({"Cannot process" : str(e)}, 500)

# @app.route("/all", methods=["POST"])
# def all():
#     try:
#         file = flask.request.files['filedata']
#         r = requests.post("speech_to_text:5000/speechtotext", files=[file])
#         print (r.json())
#         re = requests.post("localhost:8989/trip", json=r.json())
#         return (re.json(), 200)
#     except Exception as e:
#         return ({"Cannot process" : str(e)}, 500)

def test(data, prov, dest):
    french_stopwords = set(stopwords.words('french'))
    filtre_stopfr =  lambda text: [token for token in text if token.lower() not in french_stopwords]
    sp_pattern = re.compile("""[\.\!\"\s\?\-\,\']+""", re.M).split
    list_d = tokenized(data, filtre_stopfr, sp_pattern)
    cities = getLines("all_gares.txt")
    depuis = getLines("depuis.txt")
    gares = get_result(list_d, depuis, cities)
    if (len(gares) != 2 or gares[0] != prov or gares[1] != dest):
        if len(gares) != 2:
            return False
        if (gares[0] != prov):
            print(f"{gares[0]} != {prov}")
        elif (gares[1] != dest):
            print(f"{gares[1]} != {dest}")
        return False
    return True


@app.route('/', methods=["GET"])
def index():
    return("It works!", 200)

def main():
    app.run(host="0.0.0.0", port=8989, debug=True)

if __name__ == '__main__':
    # nltk.download('stopwords')
    main()
