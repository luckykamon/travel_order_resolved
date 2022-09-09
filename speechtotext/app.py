from requests import request
import speech_recognition as sr
import flask
import flask_cors
import unidecode
import os
from pydub import AudioSegment

app = flask.Flask(__name__)
flask_cors.CORS(app, resources={r'/*': {'origins': '*'}})

def convert(rawFile):
    rawFile.save(rawFile.filename)
    audSeg = AudioSegment.from_file(rawFile.filename)
    audSeg.export(f"file.wav", format="wav")
    os.remove(rawFile.filename)

@app.route('/speechtotext', methods=["POST"])
def sound():
    try:
        wavFile = flask.request.files['filedata']
        if (not ".wav" in wavFile.filename):
            convert(wavFile)
        else:
            wavFile.save("./file.wav")
        r = sr.Recognizer()
        with sr.AudioFile("file.wav") as source:
            audio = r.record(source)
            try:
                data = unidecode.unidecode(r.recognize_google(audio, language="fr-FR"))
                with open("data.txt", "w") as fd:
                    fd.write(data)
                return({"data": data}, 200)
            except Exception as e:
                return({"Cannot process" : e}, 500)
    except Exception as e:
        return({"Cannot get file" : e}, 500)

def main():
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == '__main__':
    main()
