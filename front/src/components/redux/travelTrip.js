import {createSlice} from '@reduxjs/toolkit'
import {loadState} from "./localStorage"


export const travelTripSlice = createSlice({
    name: 'travelTrip',
    initialState: loadState()?.travelTrip || {
        nameDataTravelTrip: "",
    },
    reducers: {
        setNameDataTravelTrip: (state, action) => {
            state.nameDataTravelTrip = action.payload;
        },
    },
})

export const {
    setNameDataTravelTrip
} = travelTripSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched
// export const incrementAsync = (amount) => (dispatch) => {
//     setTimeout(() => {
//         dispatch(incrementByAmount(amount))
//     }, 1000)
// }


export const getNameDataTravelTrip = state => state.travelTrip.nameDataTravelTrip;


export default travelTripSlice.reducer
