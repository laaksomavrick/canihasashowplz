import { Outlet } from "react-router-dom";
import { Box, Heading, Flex } from "@chakra-ui/react";

export default function Root() {
  return (
      <Box w="100vw" h="100vh">
          <Flex alignItems="center" justifyContent="center" w="100%" maxW="3xl" margin="auto" flexDir="column" h="100%">
              <Heading p="6">canihasashowplz</Heading>
              <Outlet />
          </Flex>
      </Box>
  );
}