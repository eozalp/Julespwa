# POS & Inventory Management PWA

This project is a Point-of-Sale and Inventory Management Progressive Web App, designed to be mobile-first, offline-first, and run on resource-constrained hardware like Raspberry Pi devices.

## Technology Stack

*   **Frontend:** Vue.js 3 PWA
*   **Backend:** Python (FastAPI)
*   **Database:** CouchDB / PouchDB for seamless offline-first data synchronization.

## Project Documentation

*   [Architecture](architecture.md)
*   [Technology Stack](tech_stack.md)
*   [JSON Schemas](json_schemas.md)
*   [Offline Sync Strategy](sync_strategy.md)
*   [REST API Examples](api_examples.md)
*   [Deployment Guide](deployment_guide.md)

## Project Structure

*   `/pwa`: Contains the Vue.js-based PWA.
*   `/backend`: Contains the Python-based FastAPI backend server.

## Getting Started

1.  **Database Setup:**
    *   This project is designed to work with CouchDB or a PouchDB-Server.
    *   Follow the [Deployment Guide](deployment_guide.md) to set up your database.
    *   Ensure the PWA's service worker and the backend are configured with the correct database URL.

2.  **Backend (FastAPI):**
    *   Navigate to the `backend` directory.
    *   Create a virtual environment: `python3 -m venv venv`
    *   Activate it: `source venv/bin/activate`
    *   Install dependencies: `pip install -r requirements.txt`
    *   Run the server: `uvicorn main:app --reload`

3.  **PWA (Vue.js):**
    *   Navigate to the `pwa` directory.
    *   Run `npm install`.
    *   Run `npm run serve` to start the development server.

The PWA will be available at `http://localhost:8081` (or another port if 8080 is in use), and the backend API will be at `http://localhost:8000`.
