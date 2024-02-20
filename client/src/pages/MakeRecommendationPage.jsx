import { Button, Flex, Input, Stack, Text } from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import usePostRecommendationRequest from "../api/usePostRecommendationRequest.js";
import { useEffect } from "react";
import { usePredictionContext } from "../contexts/PredictionContext.jsx";
import { useNavigate } from "react-router-dom";
import { ErrorMessage } from "../components/ErrorMessage.jsx";


function MakeRecommendationPage() {
    const { setPredictionId } = usePredictionContext();
    const { register, handleSubmit, formState } = useForm({
        mode: "onChange",
    });

    const { data, loading, isError, post } = usePostRecommendationRequest();
    const navigate = useNavigate();

    const onSubmit = handleSubmit(async (data) => {
        const first = data.showOne;
        const second = data.showTwo;
        const third = data.showThree;
        const shows = [first, second, third];
        await post(shows);
    });

    useEffect(() => {
        if (data == null) {
            return;
        }

        const predictionId = data.prediction_id;
        setPredictionId(predictionId);
        navigate("/processing");
    }, [data]);

    return (
        <Flex flexDir="column">
            <Stack spacing={3}>
                <Text
                    fontSize="2xl"
                    color="gray.700"
                    margin="auto"
                    pb="4"
                    fontWeight="medium"
                >
                    To begin, submit three television shows you enjoy:</Text>
                <form onSubmit={onSubmit}>
                    <Stack spacing={3}>
                        <Input
                            name="showOne"
                            id="showOne"
                            placeholder="Show one" {...register("showOne", { required: true })}
                            size="lg"
                            boxShadow="sm"
                            rounded="md"
                            background="white"

                        />
                        <Input name="showTwo" id="showTwo"
                               placeholder="Show two" {...register("showTwo", { required: true })}
                               size="lg"
                               boxShadow="sm"
                               rounded="md"
                               background="white"

                        />
                        <Input name="showThree" id="showThree"
                               placeholder="Show three" {...register("showThree", { required: true })} size="lg"
                               boxShadow="sm"
                               rounded="md"
                               background="white"
                                />
                        <Button type="submit" colorScheme="blue" size="lg" boxShadow="sm"


                                isDisabled={formState.isValid === false} isLoading={formState.isSubmitting || loading}>
                            Submit
                        </Button>
                    </Stack>
                </form>
                <ErrorMessage isOpen={isError} />
            </Stack>
        </Flex>
    );
}

export default MakeRecommendationPage;
