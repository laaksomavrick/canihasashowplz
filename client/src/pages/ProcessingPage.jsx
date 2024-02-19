import { usePredictionContext } from "../contexts/PredictionContext.jsx";
import useGetPredictionRequest from "../api/useGetPredictionRequest.js";
import useInterval from "../hooks/useInterval.js";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Flex, Spinner } from "@chakra-ui/react";
import { Navigate } from "react-router-dom";


function ProcessingPage() {
    const navigate = useNavigate();
    const { predictionId, setShows } = usePredictionContext();
    const { data, get } = useGetPredictionRequest();


    if (predictionId == null) {
        return <Navigate to='/'></Navigate>
    }

    useInterval(async () => {
        if (data) {
            return;
        }
        await get(predictionId);
    }, 10000, false, [data]);

    useEffect(() => {
        if (data == null) {
            return;
        }

        setShows(data["show_titles"]);
        navigate("/results");

    }, [data]);


    return (
        <Flex justifyContent="center" alignItems="center" h="100%">
            <Spinner
  thickness='4px'
  speed='0.65s'
  emptyColor='gray.200'
  color='blue.500'
  size='xl'
/>
        </Flex>
    );
}

export default ProcessingPage;
