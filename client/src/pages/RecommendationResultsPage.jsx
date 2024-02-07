import { usePredictionContext } from "../contexts/PredictionContext.jsx";
import { Flex, ListItem, Spinner, Stack, Text, UnorderedList } from "@chakra-ui/react";

function RecommendationResultsPage() {
    const { shows } = usePredictionContext();

    if (shows == null) {
        // TODO: redirect to make prediction page
        return
    }

  return (
     <Flex alignItems="center" w="100%" h="100%" flexDir="column">
         <Text fontSize="2xl" mb="4">
             Recommended shows
         </Text>
         <UnorderedList>
             {shows.map(show => <ListItem key={show} fontSize="lg">{show}</ListItem>)}
         </UnorderedList>
    </Flex>
  )
}

export default RecommendationResultsPage
