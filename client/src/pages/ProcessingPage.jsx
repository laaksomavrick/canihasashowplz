import { usePredictionContext } from "../contexts/PredictionContext.jsx";
import useGetPredictionRequest from "../api/useGetPredictionRequest.js";
import useInterval from "../hooks/useInterval.js";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Flex, Spinner } from "@chakra-ui/react";

function ProcessingPage() {
    const navigate = useNavigate();
    const { predictionId, setShows } = usePredictionContext();
    const { data, get } = useGetPredictionRequest();


    if (predictionId == null) {
        // TODO: redirect back to make recommendation page
    }

    useInterval(() => {
        if (data) {
            return;
        }
        get(predictionId);
    }, 10000, false, [data]);

    useEffect(() => {
        if (data == null) {
            return;
        }

        setShows(data["show_titles"]);
        navigate("/results");

    }, [data]);


    return (
        <Flex justifyContent="center" alignItems="center" w="100%" h="100%">
            <Spinner
                thickness="4px"
                speed="0.65s"
                emptyColor="gray.200"
                color="teal.500"
                size="xl"
            />
        </Flex>
    );
}

export default ProcessingPage;
