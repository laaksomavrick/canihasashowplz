import { useState } from "react";
import { API_BASE_URL } from "../constants.js";

const usePostRecommendationRequest = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isError, setError] = useState(null);

  const post = async (shows) => {
    try {
      setLoading(true);
      const url = `${API_BASE_URL}/v1/shows/recommend`;
      const requestBody = { shows };

      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error("Oops! Something went wrong.");
      }

      const result = await response.json();
      setData(result);
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, isError, post };
};

export default usePostRecommendationRequest;
