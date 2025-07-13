Here are the proposed JSON schemas for the core data models. They are designed to be concise to minimize storage and network overhead, while still being flexible enough to support the application's features.

**Common Fields:**

*   `_id`: A unique identifier for the document. PouchDB/CouchDB requires this field. We'll use a `type:id` format for easy identification (e.g., `product:123`).
*   `_rev`: A revision token managed by PouchDB/CouchDB to handle conflicts.
*   `createdAt`: ISO 8601 timestamp for when the document was created.
*   `updatedAt`: ISO 8601 timestamp for when the document was last updated.

---

### 1. Product Schema

This schema represents a product in the inventory. It now includes a `tags` field and a `categoryId`.

```json
{
  "_id": "product:uuid-12345",
  "_rev": "1-abc...",
  "name": "Organic Apples",
  "description": "Fresh, locally sourced organic apples.",
  "sku": "APL-001",
  "price": 1.99,
  "cost": 0.75,
  "taxable": true,
  "pictures": [
    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD..."
  ],
  "categoryId": "category:fruit",
  "tags": ["organic", "fresh", "local"],
  "supplierId": "sup:local-farms",
  "stock": 150,
  "createdAt": "2023-10-27T10:00:00Z",
  "updatedAt": "2023-10-27T10:00:00Z"
}
```

**Fields:**

*   **`tags`**: An array of strings for user-defined tags.
*   **`categoryId`**: A foreign key to a `Category` document.

---

### 2. Category Schema

A simple schema for product categories.

```json
{
  "_id": "category:fruit",
  "_rev": "1-xyz...",
  "name": "Fruit",
  "description": "Fresh and frozen fruit.",
  "createdAt": "2023-10-26T09:00:00Z",
  "updatedAt": "2023-10-26T09:00:00Z"
}
```

---

### 3. StockEntry Schema

This schema represents a change in the stock level of a product.

```json
{
  "_id": "stock:uuid-67890",
  "_rev": "1-def...",
  "productId": "product:uuid-12345",
  "type": "intake", // "intake" | "adjustment" | "return"
  "quantity": 100,
  "notes": "Received new shipment from Local Farms.",
  "userId": "user:jane-doe",
  "createdAt": "2023-10-27T11:00:00Z",
  "updatedAt": "2023-10-27T11:00:00Z"
}
```

---

### 4. Sale Schema

This schema represents a single sales transaction.

```json
{
  "_id": "sale:uuid-abcde",
  "_rev": "1-ghi...",
  "items": [
    {
      "productId": "product:uuid-12345",
      "name": "Organic Apples",
      "quantity": 2,
      "price": 1.99
    }
  ],
  "subtotal": 3.98,
  "tax": 0.32,
  "total": 4.30,
  "paymentMethod": "cash",
  "userId": "user:john-doe",
  "createdAt": "2023-10-27T12:30:00Z",
  "updatedAt": "2023-10-27T12:30:00Z"
}
```

---

### 5. User Schema

A simple schema for users.

```json
{
  "_id": "user:jane-doe",
  "_rev": "1-jkl...",
  "name": "Jane Doe",
  "role": "manager", // "manager" | "cashier"
  "pin": "hashed_pin_1234",
  "createdAt": "2023-10-26T09:00:00Z",
  "updatedAt": "2023-10-26T09:00:00Z"
}
```
