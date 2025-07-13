Here are some examples of the REST API endpoints. These examples assume the API is running at `http://localhost:8080` and that the user is authenticated with a JWT bearer token.

**Authentication:**

*   All requests should include an `Authorization` header:
    `Authorization: Bearer <your_jwt_token>`

---

### Products API (`/products`)

This API is for standard CRUD operations on products. It's useful for administrative tasks that might be performed outside of the main PWA (e.g., a web-based admin panel).

#### 1. Create a Product

*   **Endpoint:** `POST /products`
*   **Description:** Adds a new product to the database.
*   **Payload:** The product JSON object.

**Example `curl` command:**

```bash
curl -X POST http://localhost:8080/products \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{
  "name": "Organic Bananas",
  "price": 0.59,
  "stock": 200
}'
```

---

#### 2. Get a Product

*   **Endpoint:** `GET /products/:id`
*   **Description:** Retrieves a single product by its ID.

**Example `curl` command:**

```bash
curl http://localhost:8080/products/product:uuid-12345 \
-H "Authorization: Bearer <your_jwt_token>"
```

---

#### 3. Update a Product

*   **Endpoint:** `PUT /products/:id`
*   **Description:** Updates an existing product.
*   **Payload:** The full product JSON object with the updated fields.

**Example `curl` command:**

```bash
curl -X PUT http://localhost:8080/products/product:uuid-12345 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{
  "name": "Organic Bananas",
  "price": 0.69,
  "stock": 190
}'
```

---

#### 4. Delete a Product

*   **Endpoint:** `DELETE /products/:id`
*   **Description:** Deletes a product from the database. In a PouchDB/CouchDB environment, this is a "soft delete" (the document is marked as `_deleted: true`).

**Example `curl` command:**

```bash
curl -X DELETE http://localhost:8080/products/product:uuid-12345 \
-H "Authorization: Bearer <your_jwt_token>"
```

---

### Sales API (`/sales`)

#### 1. Post a Sale

*   **Endpoint:** `POST /sales`
*   **Description:** Records a new sale. The payload will be a `Sale` document.

**Example `curl` command:**

```bash
curl -X POST http://localhost:8080/sales \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{
  "items": [
    { "productId": "product:uuid-12345", "quantity": 5, "price": 0.69 },
    { "productId": "product:uuid-67890", "quantity": 1, "price": 3.49 }
  ],
  "total": 6.94,
  "userId": "user:jane-doe"
}'
```

---

### Sync API (`/sync`)

This is the most important endpoint for our offline-first PWA. PouchDB will interact with this endpoint (or more accurately, with the CouchDB-compatible endpoint that PouchDB expects) to perform synchronization. While you won't typically use `curl` to interact with the sync endpoint (PouchDB handles it), here's what a batch `_bulk_docs` request looks like, which is what PouchDB uses to send changes to the server.

*   **Endpoint:** `POST /db/_bulk_docs` (This is the standard CouchDB endpoint)
*   **Description:** Allows for batch creation, updating, and deletion of documents. This is the mechanism PouchDB uses to efficiently sync a batch of changes to the server.
*   **Payload:** An object containing an array of documents.

**Example `curl` command for a batch update:**

```bash
curl -X POST http://localhost:8080/db/_bulk_docs \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_jwt_token>" \
-d '{
  "docs": [
    {
      "_id": "product:uuid-abcde",
      "name": "New Product",
      "price": 9.99,
      "stock": 50
    },
    {
      "_id": "sale:uuid-fghij",
      "items": [{ "productId": "product:uuid-abcde", "quantity": 1, "price": 9.99 }],
      "total": 9.99,
      "userId": "user:john-doe"
    },
    {
      "_id": "product:uuid-12345",
      "_rev": "2-xyz...",
      "_deleted": true
    }
  ]
}'
```

This batch contains a new product, a new sale, and a deleted product. This is how the PWA can efficiently send all offline-created data to the server in a single request. The server will process this batch and respond with the results for each document.
