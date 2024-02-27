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
import RecommendationResultsPage from "./pages/RecommendationResultsPage.jsx";
import MakeRecommendationPage from "./pages/MakeRecommendationPage.jsx";
import { PredictionContextProvider } from "./contexts/PredictionContext.jsx";
import AboutPage from "./pages/AboutPage";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Root />,
        errorElement: <ErrorPage />,
        children: [
             {
                path: "/",
                element: <MakeRecommendationPage />,
            },
            {
                path: "/processing",
                element: <ProcessingPage />,
            },
            {
                path: "/results",
                element: <RecommendationResultsPage />,
            },
            {
                path: "/about",
                element: <AboutPage />,
            },
        ]
    },
]);

const rootElement = document.getElementById("root");

ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
        <ChakraProvider>
            <PredictionContextProvider>
                <RouterProvider router={router} />
            </PredictionContextProvider>
        </ChakraProvider>
    </React.StrictMode>,
);