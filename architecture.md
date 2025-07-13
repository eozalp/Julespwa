```mermaid
graph TD
    subgraph Client-Side (PWA)
        A[UI - Svelte/JS] -- Interacts --> B{Service Worker};
        A -- Reads/Writes --> C[Local DB - Dexie.js];
        B -- Caches Assets --> D[Static Assets];
        B -- Interacts for Sync --> C;
        C -- Manages --> E[IndexedDB - PouchDB];
    end

    subgraph Server-Side
        F[API - Go/Node.js] -- CRUD --> G[Database - CouchDB/PouchDB-Server];
        F -- Auth --> H[JWT/Basic Auth];
    end

    subgraph Data Flow
        C -- Sync via Service Worker --> F;
        F -- Pushes Changes --> C;
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px;
    style B fill:#ccf,stroke:#333,stroke-width:2px;
    style C fill:#cfc,stroke:#333,stroke-width:2px;
    style F fill:#fcf,stroke:#333,stroke-width:2px;
    style G fill:#ffc,stroke:#333,stroke-width:2px;
```

### Architecture Components:

**Client-Side (Progressive Web App):**

*   **UI (Svelte/Vanilla JS):** The user interface, built with a lightweight and fast framework. It's responsible for rendering the product catalog, sales interface, and analytics. It interacts directly with the local database for all data operations, ensuring a seamless offline experience.
*   **Service Worker:** The heart of the offline capability. It acts as a network proxy, intercepting all network requests. It serves cached assets (HTML, CSS, JS, images) for instant loading and offline availability. It also manages background synchronization of data with the server.
*   **Local DB (Dexie.js):** A wrapper for IndexedDB that simplifies database operations with a clean, promise-based API. It provides the main interface for the UI to interact with the local data store.
*   **IndexedDB (PouchDB):** The underlying database technology in the browser. PouchDB is used here for its CouchDB-compatible API, which makes synchronization with a CouchDB backend seamless.

**Server-Side:**

*   **API (Go/Node.js):** A minimal REST API that handles data synchronization, user authentication, and any server-side logic. The choice between Go and Node.js will depend on performance requirements and developer familiarity.
*   **Database (CouchDB/PouchDB-Server):** The central database. CouchDB is highly recommended for its excellent master-master replication capabilities, which are perfect for this kind of distributed, occasionally-connected application. A PouchDB-Server instance on Node.js is a lighter-weight alternative.
*   **Authentication (JWT/Basic Auth):** A stateless authentication mechanism. JWT (JSON Web Tokens) or simple hashed Basic Auth will be used to secure the API endpoints without requiring a session store on the server, which keeps the backend lightweight.

### Data Flow:

*   **Online:** When the application is online, the Service Worker attempts to synchronize the local PouchDB database with the server-side CouchDB/PouchDB-Server. Changes from the client are pushed to the server, and changes from the server are pulled down to the client.
*   **Offline:** When the application is offline, all data operations (sales, inventory updates, etc.) are saved to the local PouchDB database. The Service Worker queues these changes. Once the application comes back online, the Service Worker will automatically sync the queued changes with the server.

This architecture ensures that the application is always responsive and functional, regardless of the network conditions. The use of PouchDB/CouchDB greatly simplifies the synchronization logic, and the lightweight nature of the chosen technologies makes it ideal for resource-constrained environments.
