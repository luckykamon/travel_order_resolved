import PropTypes from "prop-types"

const Trip = (props) => {

    return (
        <div style={{textAlign: "center"}}>
            <h3>Departure: {props.departure}</h3>
            <h3>Destination: {props.destination}</h3>
        </div>
    )

}

Trip.propTypes = {
    departure: PropTypes.string.isRequired,
    destination: PropTypes.string.isRequired,
}

Trip.defaultProps = {
    departure: "Loading...",
    destination: "Loading...",
}

export default Trip