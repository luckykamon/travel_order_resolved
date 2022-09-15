# import nlp_perso
import requests

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite aller à Rennes depuis Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test1"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test1"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite partir depuis Paris et aller à Rennes"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test2"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test2"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite aller a Rennes en partant de Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test3"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test3"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite aller de Rennes à Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Rennes", "Wrong departure for test4"
assert r.json()["Destination"] == "Paris", "Wrong destination for test4"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite partir de Paris pour aller à Rennes"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test5"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test5"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite aller à Rennes à partir de Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test6"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test6"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite faire Paris Rennes"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test7"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test8"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite faire Rennes Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Rennes", "Wrong departure for test9"
assert r.json()["Destination"] == "Paris", "Wrong destination for test9"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite prendre un train en provenance de Paris et a destination de Rennes"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test10"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test10"

r = requests.post("http://localhost:8989/trip", json={"data" : "Je souhaite prendre un train a destination de Rennes et en provenance de Paris"})
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["Departure"] == "Paris", "Wrong departure for test11"
assert r.json()["Destination"] == "Rennes", "Wrong destination for test11"

r = requests.post("http://localhost:8989/trip", json={"data" : ""})
assert r.status_code == 400, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
