import * as React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import * as ReactDOM from "react-dom/client";
import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";
import Root from "./routes/Root.jsx";
import ErrorPage from "./pages/ErrorPage";
import ProcessingPage from "./pages/ProcessingPage.jsx";
import PredictionResultsPage from "./pages/PredictionResultsPage.jsx";
import MakePredictionPage from "./pages/MakePredictionPage.jsx";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Root />,
        errorElement: <ErrorPage />,
        children: [
             {
                path: "/",
                element: <MakePredictionPage />,
            },
            {
                path: "/processing",
                element: <ProcessingPage />,
            },
            {
                path: "/results",
                element: <PredictionResultsPage />,
            },
        ]
    },
]);

const rootElement = document.getElementById("root");

ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
        <ChakraProvider>
            <RouterProvider router={router} />
        </ChakraProvider>
    </React.StrictMode>,
);