import { useState } from "react";
import { API_BASE_URL } from "../constants.js";

const useGetPredictionRequest = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isError, setError] = useState(null);

  const get = async (predictionId) => {
    try {
      setLoading(true);
      const params = new URLSearchParams({ prediction_id: predictionId });
      const url = `${API_BASE_URL}/v1/prediction?${params}`;

      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      // if (!response.ok) {
      //   throw new Error("Oops! Something went wrong.");
      // }

      const result = await response.json();
      setData(result);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, isError, get };
};

export default useGetPredictionRequest;
