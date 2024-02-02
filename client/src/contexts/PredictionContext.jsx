import { createContext, useContext, useState } from "react";

const PredictionContext = createContext([null, () => {}])

export const PredictionContextProvider = ({ children }) => {
    const [predictionId, setPredictionId] = useState(null);

    return <PredictionContext.Provider value={[predictionId, setPredictionId]}>{children}</PredictionContext.Provider>
}

export const usePredictionContext = () => useContext(PredictionContext);