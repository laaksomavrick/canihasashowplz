import { usePredictionContext } from "../contexts/PredictionContext.jsx";
import { Flex, Grid, ListItem, Text, UnorderedList } from "@chakra-ui/react";
import { Navigate } from "react-router-dom";
import ShowCard from "../components/ShowCard.jsx";

function RecommendationResultsPage() {
    const { shows } = usePredictionContext();

    if (shows == null || shows.length === 0) {
        return <Navigate to='/'></Navigate>
    }

  return (
     <Flex alignItems="center" flexDir="column">
         <Text
                    fontSize="2xl"
                    color="gray.700"
                    margin="auto"
                    pb="4"
                    fontWeight="medium"
                >
             The results are in:
         </Text>
         <Grid templateRows="1fr" templateColumns="1fr" gap={4}>
             {shows.map(show => <ShowCard key={show.title} show={show} />)}
         </Grid>
    </Flex>
  )
}

export default RecommendationResultsPage
