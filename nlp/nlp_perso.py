import flask
from nltk.corpus import stopwords
from nltk import word_tokenize
import re
import flask_cors

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

def tokenized(data,filtre_stopfr, sp_pattern):
    d = " ".join(str(x) for x in sp_pattern(data))
    return (filtre_stopfr(word_tokenize(d, language="french")))

@app.route("/trip", methods=["POST"])
def trip():
    try:
        if not 'data' in flask.request.json:
            raise Exception("No data in json")
        data = flask.request.json['data']
        french_stopwords = set(stopwords.words('french'))
        filtre_stopfr =  lambda text: [token for token in text if token.lower() not in french_stopwords]
        sp_pattern = re.compile("""[\.\!\"\s\?\-\,\']+""", re.M).split
        list_d = tokenized(data, filtre_stopfr, sp_pattern)
        cities = getLines("all_gares.txt")
        depuis = getLines("depuis.txt")
        gares = get_result(list_d, depuis, cities)
        if len(gares) != 2:
            return ({f"Not exactly 2 station given" : gares}, 400)
        return ({"Departure": gares[0], "Destination": gares[1]})
    except Exception as e:
        return ({"Cannot process" : str(e)}, 500)

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
    main()
