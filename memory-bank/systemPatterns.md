# System Patterns *Optional*

This file documents recurring patterns and standards used in the project.
It is optional, but recommended to be updated as the project evolves.
2025-08-03 18:22:14 - Log of updates made.

*

## Coding Patterns

*   **Backend:**
    *   Flask blueprints are used to organize routes for each feature.
    *   Services are separated from routes to encapsulate business logic.
    *   `yfinance` and `pandas-ta` are used for data fetching and technical analysis.
*   **Frontend:**
    *   React functional components with hooks are used for UI.
    *   Material-UI is used for UI components.
    *   `axios` is used for making API requests.
    *   `react-router-dom` is used for client-side routing.

## Architectural Patterns

*   The application is a single-page application (SPA) with a separate backend API.
*   The backend is a RESTful API built with Flask.

## Testing Patterns

*   Manual testing has been performed on all endpoints.