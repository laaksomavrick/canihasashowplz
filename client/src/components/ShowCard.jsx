import { Button, Card, CardBody, CardFooter, Heading, Image, Stack, Text } from "@chakra-ui/react";

function ShowCard({ show }) {
    const title = show.title;
    const logoUrl = show.logo_url;
    const description = show.description;
    const airDate = new Date(show.air_date).getFullYear();
    const rating = Math.round(show.rating * 10) / 10

    return (
        <Card
            direction={{ base: "column", sm: "row" }}
            overflow="hidden"
            variant="outline"
        >
            <Image
                objectFit="cover"
                maxW={{ base: "100%", sm: "200px" }}
                src={logoUrl}
                alt={title}
            />

            <Stack>
                <CardBody>
                    <Heading size="md">{title} ({airDate})</Heading>

                    <Text py="2">
                        {description}
                    </Text>
                </CardBody>

                <CardFooter>
                    <Text fontWeight="medium" fontSize="xl">
                        Rating: {rating}
                    </Text>
                </CardFooter>
            </Stack>
        </Card>
    );
}

export default ShowCard