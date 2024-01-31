import { Flex, Text, Input, Stack, Button } from "@chakra-ui/react";
import { useState } from "react";
import { useForm } from 'react-hook-form';

function MakePredictionPage() {
    const { register, handleSubmit, errors, formState } = useForm({
        mode: 'onChange',
    });

    const onSubmit = handleSubmit(async (data) => {
        const first = data.showOne;
        const second = data.showTwo;
        const third = data.showThree
        const shows = [first, second, third]

        console.log(shows)
    });

    return (
        <Flex flexDir="column">
            <Stack spacing={3}>
                <Text fontSize="xl">Please enter three shows you enjoy to generate a recommendation</Text>
                <form onSubmit={onSubmit}>
                    <Stack spacing={3}>
                        <Input name="showOne" id="showOne" placeholder="Show one" {...register("showOne", { required: true })} size="lg" />
                        <Input name="showTwo" id="showTwo" placeholder="Show two" {...register("showTwo", { required: true })} size="lg" />
                        <Input name="showThree" id="showThree" placeholder="Show three" {...register("showThree", { required: true })} size="lg" />
                        <Button type="submit" colorScheme='teal' size='lg' isDisabled={formState.isValid === false} isLoading={formState.isSubmitting}>
                            Submit
                        </Button>
                    </Stack>
                </form>
            </Stack>
        </Flex>
    );
}

export default MakePredictionPage;
