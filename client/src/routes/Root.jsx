import { Outlet } from "react-router-dom";
import { Box, Heading, Flex, Grid } from "@chakra-ui/react";

export default function Root() {
  return (
      <Box w="100vw" h="100vh" background="red.600">
          <Grid
              templateRows='minmax(100px, max-content) 1fr'
              w="100%"
              maxW="3xl"
              h="100%"
              margin="auto"
          >
              <Flex px="6" justifyContent="center">
                  <Heading
                      size="2xl"
                      py="6"
                      color="white"
                      style={{
                          'text-shadow': '5px 5px 0 #000, -1px 1px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000'
                      }}
                  >canihasashowplz</Heading>
              </Flex>
              <Box px="6">
                  <Outlet />
              </Box>
          </Grid>
      </Box>
  );
}