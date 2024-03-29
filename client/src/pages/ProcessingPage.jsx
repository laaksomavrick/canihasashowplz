import { usePredictionContext } from "../contexts/PredictionContext.jsx";
import useGetPredictionRequest from "../api/useGetPredictionRequest.js";
import useInterval from "../hooks/useInterval.js";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Flex, Spinner, Text, Grid } from "@chakra-ui/react";
import { Navigate } from "react-router-dom";


function ProcessingPage() {
    const navigate = useNavigate();
    const { predictionId, setShows } = usePredictionContext();
    const { data, get } = useGetPredictionRequest();


    if (predictionId == null) {
        return <Navigate to="/"></Navigate>;
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

        setShows(data["shows"]);
        navigate("/results");

    }, [data]);


    return (
         <Grid
              templateRows='minmax(100px, max-content) 1fr minmax(100px, max-content)'
              w="100%"
              maxW="3xl"
              h="100%"
              margin="auto"
          >
             <Text
                    fontSize="2xl"
                    color="gray.700"
                    margin="auto"
                    pb="4"
                    fontWeight="medium"
                >
                    Crunching some numbers, please wait...</Text>
                     <Flex justifyContent="center" alignItems="center" h="100%" flexDir="column">

            <Spinner
                thickness="4px"
                speed="0.65s"
                emptyColor="gray.200"
                color="blue.500"
                size="xl"
            />
        </Flex>
         </Grid>

    );
}

export default ProcessingPage;
