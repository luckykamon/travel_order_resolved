import requests

files=[('filedata',('3_Allee_Raymond_Cornon.wav', open('./3_Allee_Raymond_Cornon.wav','rb')))]
r = requests.post("http://localhost:6000/speechtotext", files=files)
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["data"].lower() == "je veux aller a paris en passant par nantes depuis rennes"
print("3_Allee_Raymond_Cornon.wav --> OK")

files=[('filedata',('3_Allee_Raymond_Cornon.qt', open('./3_Allee_Raymond_Cornon.qt','rb')))]
r = requests.post("http://localhost:6000/speechtotext", files=files)
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["data"].lower() == "je veux aller a paris en passant par nantes depuis rennes"
print("3_Allee_Raymond_Cornon.qt --> OK")

files=[('filedata',('pariscarcassone.wav', open('./pariscarcassone.wav','rb')))]
r = requests.post("http://localhost:6000/speechtotext", files=files)
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["data"].lower() == "je cherche un train de paris a carcassonne", f"Content : {r.json()}"
print("pariscarcassone.wav --> OK")

files=[('filedata',('pariscarcassone.mp3', open('./pariscarcassone.mp3','rb')))]
r = requests.post("http://localhost:6000/speechtotext", files=files)
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["data"].lower() == "je cherche un train de paris a carcassonne", f"Content : {r.json()}"
print("pariscarcassone.mp3 --> OK")

