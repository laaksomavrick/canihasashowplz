import { createContext, useContext, useState } from "react";

const PredictionContext = createContext([null, () => {}])

export const PredictionContextProvider = ({ children }) => {
    const [predictionId, setPredictionId] = useState(null);
    const [shows, setShows] = useState([])

    const value = {
        predictionId,
        shows,
        setPredictionId,
        setShows
    }

    return <PredictionContext.Provider value={value}>{children}</PredictionContext.Provider>
}

export const usePredictionContext = () => useContext(PredictionContext);