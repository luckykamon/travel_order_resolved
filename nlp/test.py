import requests

nb_valid_test = 1
nb_invalid_test = 1
PARIS="Paris"
RENNES="Rennes"

def make_test_trip_valid(data: str, expected_departure: str, expected_destination: str, expected_code: int):
    global nb_valid_test
    r = requests.post("http://localhost:8989/trip", json={"data" : data})
    assert r.status_code == expected_code, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
    departure = r.json()["Departure"]
    destination = r.json()["Destination"]
    assert departure == expected_departure, f"Wrong departure for test {nb_valid_test}. Expected \"{expected_departure}\", got \"{departure}\""
    assert destination == expected_destination, f"Wrong destination for test {nb_valid_test}. Expected \"{expected_destination}\", got \"{destination}\""
    print(f"test {nb_valid_test} OK")
    nb_valid_test += 1

def make_test_trip_invalid(data: str, expected_code: int):
    global nb_invalid_test
    r = requests.post("http://localhost:8989/trip", json={"data" : data})
    assert r.status_code == expected_code, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
    print(f"test invalid {nb_invalid_test} OK")
    nb_invalid_test += 1

if __name__ == "__main__":
    make_test_trip_valid(data="Je souhaite aller à Rennes depuis Paris", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)
    make_test_trip_valid(data="Je souhaite partir depuis Paris et aller à Rennes", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)
    make_test_trip_valid(data="Je souhaite aller a Rennes en partant de Paris", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)
    make_test_trip_valid(data="Je souhaite aller de Rennes à Paris", expected_departure=RENNES, expected_destination=PARIS, expected_code=200)
    make_test_trip_valid(data="Je souhaite partir de Paris pour aller à Rennes", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)
    make_test_trip_valid(data="Je souhaite aller à Rennes à partir de Paris", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)
    make_test_trip_valid(data="Je souhaite faire Paris Rennes", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)
    make_test_trip_valid(data="Je souhaite faire Rennes Paris", expected_departure=RENNES, expected_destination=PARIS, expected_code=200)
    make_test_trip_valid(data="Je souhaite prendre un train en provenance de Paris et a destination de Rennes", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)
    make_test_trip_valid(data="Je souhaite prendre un train a destination de Rennes et en provenance de Paris", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)
    make_test_trip_valid(data="Je souhaite prendre un train a destination de Rennes et en provenance de Pariss", expected_departure=PARIS, expected_destination=RENNES, expected_code=200)

    make_test_trip_invalid(data="", expected_code=400)