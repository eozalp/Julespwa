This guide provides instructions for deploying the backend server in a resource-constrained environment like a Raspberry Pi. We'll cover two primary scenarios.

**Prerequisites:**

*   A Raspberry Pi (3 or 4 recommended) with Raspberry Pi OS (or any other Linux distro).
*   SSH access to the Raspberry Pi.
*   A static IP address configured for the Pi on your local network.

---

### Scenario 1: Python/FastAPI Backend + CouchDB

This is a robust and highly performant setup. FastAPI provides a fast, modern API, and CouchDB provides a battle-tested sync solution.

**1. Install Python & Pip:**

```bash
# On the Raspberry Pi
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
```

**2. Install CouchDB:**

```bash
# On the Raspberry Pi
sudo apt-get install -y couchdb

# Follow the on-screen prompts. Choose 'standalone' mode.
# Set an admin username and password. Note these down.
# Bind address: set to 0.0.0.0 to allow access from other devices on the network.
```

**3. Configure CouchDB:**

*   Access the CouchDB web interface (Fauxton) at `http://<pi_ip_address>:5984/_utils/`.
*   Create a new database named `pos-db`.
*   Create a new user with read/write permissions to the `pos-db` database. This user will be used by the FastAPI backend.

**4. Deploy and Run the FastAPI Application:**

*   Copy your Python project files to the Raspberry Pi.
*   Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
*   Run the application using an ASGI server like `uvicorn`:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080
    ```
*   **For production:** Use a process manager like `systemd` to run the application as a service, so it automatically restarts on boot or if it crashes.

---

### Scenario 2: Python/FastAPI Backend + PouchDB-Server

This is a lighter-weight alternative if you want to avoid a full CouchDB installation.

**1. Install Node.js (for PouchDB-Server):**

```bash
# On the Raspberry Pi
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**2. Install and Run `pouchdb-server`:**

*   Install `pouchdb-server` globally:
    ```bash
    npm install -g pouchdb-server
    ```
*   Run `pouchdb-server`:
    ```bash
    pouchdb-server --port 5984 --host 0.0.0.0
    ```
    This can be managed with a process manager like `pm2`.

**3. Deploy and Run the FastAPI Application:**

*   Follow the same steps as in Scenario 1 to deploy the FastAPI application.
*   Configure your FastAPI application to connect to the `pouchdb-server` instance at `http://127.0.0.1:5984`.

---

### PWA (Vue.js) Deployment

The Vue.js PWA is a set of static files (HTML, CSS, JavaScript).

1.  **Build the PWA:**
    *   On your development machine, run the build command: `npm run build`.
2.  **Deploy the Static Files:**
    *   You can serve the static files from the same FastAPI backend or use a dedicated web server.
    *   Using a lightweight web server like `nginx` or `caddy` is recommended.

**Example with Caddy:**

```bash
# Install Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Create a Caddyfile
sudo nano /etc/caddy/Caddyfile
```

Add the following to your `Caddyfile`:

```
your_domain_or_pi_ip_address {
    # Path to your Vue.js build output (usually in the 'dist' folder)
    root * /path/to/your/pwa/dist
    file_server

    # Proxy API requests to the FastAPI backend
    reverse_proxy /api/* http://localhost:8080
}
```

This configuration tells Caddy to serve your PWA files and to proxy any requests to `/api/*` to your backend server running on port 8080. This is a clean and efficient way to serve both the frontend and backend from a single entry point.
