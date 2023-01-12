import {useEffect, useState} from "react";
import PropTypes from "prop-types";
import Trip from "./Trip";
import {useSelector} from "react-redux";
import {getNameDataTravelTrip} from "../redux/travelTrip";

const TripElement = () => {
    const [trip_Element, setTrip_Element] = useState({
        "Departure": "",
        "Destination": ""
    });

    const dataTravelTrip = useSelector(getNameDataTravelTrip);


    useEffect(() => {

            let myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            let raw = JSON.stringify({
                "data": dataTravelTrip
            });

            let requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw,
                redirect: 'follow'
            };

            fetch(process.env.REACT_APP_HOST_BACK_trip + "/trip", requestOptions)
                .then(response => response.text())
                .then(result => {
                    setTrip_Element(JSON.parse(result))
                })
                .catch(error => console.log('error', error));

        }, [dataTravelTrip]
    )

    return (
        <Trip departure={trip_Element.Departure} destination={trip_Element.Destination}/>
    )
}

export default TripElement