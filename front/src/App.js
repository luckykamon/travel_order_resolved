import Typography from '@mui/material/Typography';
import PropTypes from "prop-types";
import {useEffect, useRef, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import TripElement from "./components/Trip/TripElement";
import TextField from '@mui/material/TextField';
import {getNameDataTravelTrip, setNameDataTravelTrip} from "./components/redux/travelTrip";
import {Button} from "@mui/material";

const AudioRecorder = () => {

    navigator.mediaDevices.getUserMedia({audio: true})
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            const audioChunks = [];
            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
                console.log(audioChunks)
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks);
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                console.log(audio)
                // audio.play();


                var formdata = new FormData();
                formdata.append("filedata", audioBlob, "19 Boulevard St-Conwoïon.m4a");

                var requestOptions = {
                    method: 'POST',
                    body: formdata,
                    redirect: 'follow'
                };

                fetch("http://localhost:6000/speechtotext", requestOptions)
                    .then(response => response.text())
                    .then(result => console.log(result))
                    .catch(error => console.log('error', error));


            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 3000);
        });
}


const App = () => {

    const dispatch = useDispatch();

    const updateTravelTrip = (e) => {
        dispatch(setNameDataTravelTrip(e.target.value))
    }

    return (
        <div style={{textAlign: "center"}}>
            <Typography variant="h3" gutterBottom>
                T-AIA-901-REN
            </Typography>
            <br/>

            <Button color="primary" onClick={AudioRecorder} size="md" variant="solid">Play</Button>

            <br/> <br/>

            <TextField id="TranscriptionAudio" label="Transcription audio" variant="outlined"
                       onChange={updateTravelTrip}/>

            <TripElement/>


        </div>
    );
}


export default App;
