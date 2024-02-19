import { Outlet } from "react-router-dom";
import { Box, Heading, Flex, Grid } from "@chakra-ui/react";

export default function Root() {
  return (
      <Box w="100vw" h="100vh" background="gray.50">
          <Grid
              templateRows='minmax(100px, max-content) 1fr minmax(100px, max-content)'
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
                          'text-shadow': '4px 4px 0 #2D3748, -1px 1px 0 #2D3748, -1px -1px 0 #2D3748, 1px -1px 0 #2D3748'
                      }}
                  >canihasashowplz?</Heading>
              </Flex>
              <Box px="6">
                  <Outlet />
              </Box>
          </Grid>
      </Box>
  );
}