Here are the proposed JSON schemas for the core data models. They are designed to be concise to minimize storage and network overhead, while still being flexible enough to support the application's features.

**Common Fields:**

*   `_id`: A unique identifier for the document. PouchDB/CouchDB requires this field. We'll use a `type:id` format for easy identification (e.g., `product:123`).
*   `_rev`: A revision token managed by PouchDB/CouchDB to handle conflicts.
*   `createdAt`: ISO 8601 timestamp for when the document was created.
*   `updatedAt`: ISO 8601 timestamp for when the document was last updated.

---

### 1. Product Schema

This schema represents a product in the inventory. It now includes a `pictures` field to store multiple base64-encoded images.

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
    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD...",
    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD..."
  ],
  "categoryId": "cat:fruit",
  "supplierId": "sup:local-farms",
  "stock": 150,
  "createdAt": "2023-10-27T10:00:00Z",
  "updatedAt": "2023-10-27T10:00:00Z"
}
```

**Fields:**

*   `name`, `description`: Human-readable product information.
*   `sku`: Stock Keeping Unit, a unique identifier for the product.
*   `price`, `cost`: The retail price and the cost of the product.
*   `taxable`: A boolean to indicate if sales tax should be applied.
*   **`pictures`**: An array of base64-encoded strings. Each string represents a full image, allowing for multiple pictures per product. This is ideal for an offline-first approach as the images are stored directly with the product data.
*   `categoryId`, `supplierId`: Foreign keys to other documents (e.g., `category:fruit`, `supplier:local-farms`).
*   `stock`: The current stock level. This will be updated by sales and stock entries.

---

### 2. StockEntry Schema

This schema represents a change in the stock level of a product, either from a new shipment (intake) or a manual adjustment (e.g., stock count).

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

### 3. Sale Schema

This schema represents a single sales transaction, which can include multiple items.

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
    },
    {
      "productId": "product:uuid-67890",
      "name": "Whole Wheat Bread",
      "quantity": 1,
      "price": 3.49
    }
  ],
  "subtotal": 7.47,
  "tax": 0.60,
  "total": 8.07,
  "paymentMethod": "cash", // "cash" | "card"
  "userId": "user:john-doe",
  "createdAt": "2023-10-27T12:30:00Z",
  "updatedAt": "2023-10-27T12:30:00Z"
}
```

---

### 4. User Schema

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
