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

console.log(import.meta.env.VITE_API_BASE_URL)

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