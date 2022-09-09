import requests

files=[('filedata',('3_Allee_Raymond_Cornon.wav',open('./3_Allee_Raymond_Cornon.wav','rb')))]
r = requests.post("http://localhost:5000/speechtotext", files=files)
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["data"].lower() == "je veux aller a paris en passant par nantes depuis rennes"

files=[('filedata',('pariscarcassone.mp3',open('./pariscarcassone.mp3','rb')))]
r = requests.post("http://localhost:5000/speechtotext", files=files)
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}, content : {r.content}"
assert r.json()["data"].lower() == "je cherche un train de paris à carcassonne"
