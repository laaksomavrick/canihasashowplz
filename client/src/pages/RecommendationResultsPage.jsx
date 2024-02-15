import { usePredictionContext } from "../contexts/PredictionContext.jsx";
import { Flex, ListItem, Text, UnorderedList } from "@chakra-ui/react";
import { Navigate } from "react-router-dom";

function RecommendationResultsPage() {
    const { shows } = usePredictionContext();

    if (shows == null || shows.length === 0) {
        return <Navigate to='/'></Navigate>
    }

  return (
     <Flex alignItems="center" flexDir="column">
         <Text fontSize="2xl" mb="4">
             Recommended shows
         </Text>
         <UnorderedList>
             {shows.map(show => <ListItem key={show} fontSize="xl">{show}</ListItem>)}
         </UnorderedList>
    </Flex>
  )
}

export default RecommendationResultsPage