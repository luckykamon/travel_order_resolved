# import nlp_perso
import requests

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite aller à Rennes depuis Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test1"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite partir depuis Paris et aller à Rennes"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test1"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite aller a Rennes en partant de Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test1"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite aller de Rennes à Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Rennes", "Wrong departure for test1"
assert r.json()["Destination"] == "Paris", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite partir de Paris pour aller à Rennes"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test1"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite aller à Rennes à partir de Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test1"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite faire Paris Rennes"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test1"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite faire Rennes Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Rennes"] == "Paris", "Wrong departure for test1"
assert r.json()["Paris"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite prendre un train en provenance de Paris et a destination de Rennes"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Rennes"] == "Paris", "Wrong departure for test1"
assert r.json()["Paris"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", "Je souhaite prendre un train a destination de Rennes et en provenance de Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Rennes"] == "Paris", "Wrong departure for test1"
assert r.json()["Paris"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data", ""})
assert r.status_code == 400, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
