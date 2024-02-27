import { Flex, Link, Text } from "@chakra-ui/react";

export default function AboutPage() {

  return (
    <Flex flexDir="column">
         <Text
                    fontSize="xl"
                >
             canihasashowplz is a television show recommendation engine utilizing a{' '}<Link color="blue.500" isExternal href="https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm">nearest neighbors</Link> algorithm, intended as a hobby project to explore training AI/ML models, serving them as a service, and handling their operation (MLOps).
         </Text>
        <br></br>
        <Text fontSize="xl">
            As users interact with the service to receive recommendations, they are also training the model to improve the recommendations it makes. This is likely similar to how services such as Amazon recommends products or Spotify recommends music: the algorithm doesn't need to understand the products or the music, but instead observes and uses the network based on user's preferences.
        </Text>
        <br></br>
        <Text fontSize="xl">
            All code for this project is open source and is available for exploration via{' '}<Link color="blue.500" isExternal href="https://github.com/laaksomavrick/canihasashowplz">GitHub</Link>.
        </Text>
        <br></br>
        <Text fontSize="xl">
            The author, Mavrick Laakso (that's me), also authors a blog available{' '}<Link color="blue.500" isExternal href="https://www.technoblather.ca?utm_source=canihasashowplz">here</Link>. You'll likely see a detailed reflection of my experience building this service there shortly.
        </Text>
        <br></br>
    </Flex>
  );
}