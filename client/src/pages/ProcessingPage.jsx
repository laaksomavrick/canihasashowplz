import { usePredictionContext } from "../contexts/PredictionContext.jsx";

function ProcessingPage() {
    const [predictionId,] = usePredictionContext();

  return (
    <div>
        ProcessingPage
        {predictionId}
    </div>
  )
}

export default ProcessingPage
