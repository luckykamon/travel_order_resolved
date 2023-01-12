import {configureStore} from '@reduxjs/toolkit';
import counterReducer from './travelTrip';
import {saveState} from "./localStorage"

const store = configureStore({
    reducer: {
        travelTrip: counterReducer
    },

})

store.subscribe(() => {
    saveState(store.getState())
})


export default store;
