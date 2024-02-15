import { Alert, AlertIcon, AlertTitle } from '@chakra-ui/react';
import React from 'react';

export const ErrorMessage = ({
    isOpen,
    message = 'Oops! Something went wrong',
    ...rest
}) => {
    if (!isOpen) {
        return null;
    }

    return (
        <Alert status='error' {...rest}>
            <AlertIcon />
            <AlertTitle mr={2}>{message}</AlertTitle>
        </Alert>
    );
};