This guide provides instructions for deploying the backend server in a resource-constrained environment like a Raspberry Pi. We'll cover two primary scenarios.

**Prerequisites:**

*   A Raspberry Pi (3 or 4 recommended) with Raspberry Pi OS (or any other Linux distro).
*   SSH access to the Raspberry Pi.
*   A static IP address configured for the Pi on your local network.

---

### Scenario 1: Go Backend + CouchDB

This is the most robust and recommended setup. Go provides a single, efficient binary, and CouchDB provides a battle-tested sync solution.

**1. Install Go:**

```bash
# On your development machine (not the Pi), build the Go application for Linux ARM
GOOS=linux GOARCH=arm GOARM=6 go build -o pos-server .

# On the Raspberry Pi
sudo apt-get update
sudo apt-get install -y golang
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
*   Create a new user with read/write permissions to the `pos-db` database. This user will be used by the Go backend.

**4. Deploy and Run the Go Application:**

*   Copy the `pos-server` binary from your development machine to the Raspberry Pi using `scp`.
*   Create a configuration file (`config.json`) for the Go application:
    ```json
    {
      "db_username": "your_couchdb_user",
      "db_password": "your_couchdb_password",
      "db_host": "127.0.0.1",
      "db_port": 5984,
      "jwt_secret": "a_very_secret_key"
    }
    ```
*   Run the application:
    ```bash
    ./pos-server
    ```
*   **For production:** Use a process manager like `systemd` to run the application as a service, so it automatically restarts on boot or if it crashes.

---

### Scenario 2: Node.js Backend + PouchDB-Server

This is a lighter-weight alternative, ideal for even more constrained environments or if you prefer a pure JavaScript stack.

**1. Install Node.js:**

```bash
# On the Raspberry Pi
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**2. Set up the Node.js Application:**

*   Copy your Node.js project files to the Raspberry Pi.
*   Install dependencies:
    ```bash
    npm install
    ```
*   The application should be configured to use `pouchdb-server`. You can either run `pouchdb-server` as a separate process or embed it within your Node.js application.

**3. Running `pouchdb-server`:**

*   Install `pouchdb-server` globally:
    ```bash
    npm install -g pouchdb-server
    ```
*   Run `pouchdb-server`:
    ```bash
    pouchdb-server --port 5984 --host 0.0.0.0
    ```
    This will store data in the current directory. You can specify a different directory with the `-d` flag.

**4. Deploy and Run the Node.js Application:**

*   If your Node.js app is separate from `pouchdb-server`, configure it to connect to `http://127.0.0.1:5984`.
*   Run your application:
    ```bash
    node server.js
    ```
*   **For production:** Use a process manager like `pm2` to manage the Node.js process.
    ```bash
    npm install -g pm2
    pm2 start server.js
    pm2 startup # This will generate a command to run on boot
    ```

---

### PWA Deployment

The PWA itself is just a set of static files (HTML, CSS, JavaScript).

1.  **Build the PWA:**
    *   Run the build command for your chosen framework (e.g., `npm run build` for Svelte).
2.  **Deploy the Static Files:**
    *   You can serve the static files from the same Go or Node.js backend.
    *   Alternatively, you can use a lightweight web server like `nginx` or `caddy` on the Raspberry Pi to serve the files. `caddy` is particularly easy to set up with automatic HTTPS.

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
    root * /path/to/your/pwa/build
    file_server
    reverse_proxy /api/* http://localhost:8080
}
```

This configuration tells Caddy to serve your PWA files and to proxy any requests to `/api/*` to your backend server running on port 8080. This is a clean and efficient way to serve both the frontend and backend from a single entry point.
