import requests

files=[('filedata',('3_Allee_Raymond_Cornon.wav',open('./3_Allee_Raymond_Cornon.wav','rb')))]
r = requests.post("http://localhost:5000/speechtotext", files=files)
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}"
assert r.json()["data"].lower() == "je veux aller a paris en passant par nantes depuis rennes"

files=[('filedata',('3_Allee_Raymond_Cornon.qt',open('./3_Allee_Raymond_Cornon.qt','rb')))]
r = requests.post("http://localhost:5000/speechtotext", files=files)
assert r.status_code == 200, f"STATUS CODE ERROR : {r.status_code}"
assert r.json()["data"].lower() == "je veux aller a paris en passant par nantes depuis rennes"
