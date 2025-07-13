# POS & Inventory Management PWA

This project is a Point-of-Sale and Inventory Management Progressive Web App, designed to be mobile-first, offline-first, and run on resource-constrained hardware like Raspberry Pi devices.

## Project Documentation

*   [Architecture](architecture.md)
*   [Technology Stack](tech_stack.md)
*   [JSON Schemas](json_schemas.md)
*   [Offline Sync Strategy](sync_strategy.md)
*   [REST API Examples](api_examples.md)
*   [Deployment Guide](deployment_guide.md)

## Project Structure

*   `/pwa`: Contains the Svelte-based PWA.
*   `/backend`: Contains the Go-based backend server.

## Getting Started

1.  **Backend:**
    *   Navigate to the `backend` directory.
    *   Run `go mod tidy`.
    *   Run `go run main.go`.

2.  **PWA:**
    *   Navigate to the `pwa` directory.
    *   Run `npm install`.
    *   Run `npm run dev`.

3.  **Database:**
    *   This project is designed to work with CouchDB or a PouchDB-Server.
    *   Follow the [Deployment Guide](deployment_guide.md) to set up your database.
    *   Make sure the PWA's service worker and the backend are configured with the correct database URL.
