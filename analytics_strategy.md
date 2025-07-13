This document outlines the strategy for implementing client-side analytics to power the "Insights" page. All calculations will be performed within the PWA to ensure full offline functionality.

### 1. Core Principle: On-Demand Calculation

Instead of trying to maintain a separate, pre-calculated set of analytics data, we will perform the calculations on-demand when the user visits the Insights page. Given the scale of data on a single POS device, this approach is more than performant enough and greatly simplifies the application logic.

### 2. Data Source

The primary data source for all analytics will be the `sales` collection in PouchDB. Each `Sale` document contains an array of `items` sold, which is all we need to calculate product performance.

### 3. Analytics Calculation Process

We will create an `AnalyticsService` in the Vue.js application. This service will be responsible for all analytics-related calculations.

1.  **Fetch All Sales Data:**
    *   The service will fetch all `Sale` documents from PouchDB.
    *   `const allSales = await db.sales.allDocs({ include_docs: true });`

2.  **Aggregate Sales Data:**
    *   The service will process the array of sales to create an aggregated map of product performance.
    *   The process will look like this:
        a.  Initialize an empty object, `productPerformance = {}`.
        b.  Iterate through each `sale` document.
        c.  For each `item` in the `sale.items` array:
            i.  If the `item.productId` is not yet a key in `productPerformance`, add it.
            ii. Increment the `unitsSold` for that product.
            iii. Add to the `totalRevenue` for that product.
            iv. Store the `sale.createdAt` timestamp to track when the last sale occurred.

3.  **The `productPerformance` Object:**
    *   The resulting `productPerformance` object will look something like this:
        ```json
        {
          "product:uuid-12345": {
            "productId": "product:uuid-12345",
            "unitsSold": 150,
            "totalRevenue": 298.50,
            "lastSold": "2023-10-27T12:30:00Z"
          },
          "product:uuid-67890": {
            "productId": "product:uuid-67890",
            "unitsSold": 75,
            "totalRevenue": 261.75,
            "lastSold": "2023-10-27T12:30:00Z"
          }
        }
        ```

4.  **Combining with Product Data:**
    *   The `Insights.vue` component will call the `AnalyticsService` to get the `productPerformance` data.
    *   It will then fetch all `Product` documents from PouchDB.
    *   It will combine the `productPerformance` data with the `Product` data to create a rich array of objects that can be easily displayed in the UI. Each object in the array will contain the full product details plus the calculated performance metrics.

### 4. Sorting and Filtering Logic

*   **Sorting:** The sorting logic will be implemented in the `Insights.vue` component. It will use standard JavaScript array `sort()` methods on the combined data array. For example, to sort by "Best Selling":
    ```javascript
    computed: {
      sortedProducts() {
        return this.productsWithPerformance.sort((a, b) => b.unitsSold - a.unitsSold);
      }
    }
    ```
*   **Filtering:** The filtering logic will also be in the `Insights.vue` component. It will use `filter()` methods on the data array based on the user's selections. For example, to filter by category:
    ```javascript
    computed: {
      filteredProducts() {
        return this.sortedProducts.filter(p => p.categoryId === this.selectedCategory);
      }
    }
    ```
    Multiple filters can be chained together.

### 5. Performance Considerations

*   For a typical small to medium-sized business, the number of sales records stored locally will be manageable (thousands to tens of thousands). JavaScript can process this volume of data very quickly.
*   The calculations will only run when the user navigates to the Insights page, so it won't impact the performance of the core POS functionalities.
*   As an optimization for very large datasets, we could explore caching the calculated `productPerformance` object in IndexedDB and only updating it with new sales since the last calculation. However, the on-demand approach should be sufficient for the initial implementation.

This strategy provides a clear and efficient way to generate the required analytics for the Insights page, ensuring it works seamlessly offline and integrates well with the existing data structure.
