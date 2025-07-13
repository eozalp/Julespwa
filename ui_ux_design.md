This document outlines the UI/UX design approach for the POS PWA, focusing on the newly specified functional requirements.

### Core Principles

1.  **Mobile-First, but Desktop-Friendly:** The UI will be designed for touch on mobile devices, but will also be fully navigable and usable with a keyboard and mouse on a desktop.
2.  **Picture-Centric:** Product images are central to the user experience. They will be large, clear, and interactive.
3.  **Efficiency and Speed:** Workflows for common tasks (selling, counting, receiving) will be optimized to require the minimum number of taps/clicks.

---

### 1. Main Navigation & Layout

*   A simple, clear navigation bar at the bottom (mobile) or side (desktop) will provide access to the main sections: **Sell**, **Products**, **Receiving**, **Counting**, and **Analytics**.
*   The layout will be responsive, adapting to different screen sizes.

---

### 2. Picture-Centric Product Interface

*   **Product List/Grid:** Products will be displayed in a grid with large thumbnails. Tapping/clicking a product will bring up a detailed view.
*   **Product Detail View:**
    *   A carousel or gallery will display all pictures for the product.
    *   Users can swipe or click through the images.
    *   A "Camera" button will allow the user to take a new picture or select one from the gallery. The image will be converted to a base64 string and added to the product's `pictures` array.
    *   Key information (name, price, stock) will be clearly visible.

---

### 3. Keyboard-Friendly Desktop GUI

*   **Tab Navigation:** All interactive elements (buttons, inputs, etc.) will be reachable via the `Tab` key.
*   **Shortcuts:**
    *   `F1`: Focus the main search bar.
    *   `Enter`: Select the highlighted item in a list or confirm a dialog.
    *   `Esc`: Close a modal or go back.
    *   `Arrow Keys`: Navigate lists and grids.
*   **Quick Search:** The main product search will be a central, always-accessible feature.

---

### 4. Workflows

#### a. Selling

1.  The "Sell" screen will feature a grid of frequently sold products for quick access.
2.  The user can use the **barcode scanner** or the **quick search** to add products to the cart.
3.  The cart will be a running list on the side of the screen.
4.  The user can adjust quantities and remove items from the cart.
5.  Clicking "Checkout" will lead to a simple payment screen.

#### b. Receiving Stock

1.  The "Receiving" screen will have a prominent "Scan Barcode" button.
2.  The user can scan a product's barcode to bring up its details.
3.  A simple form will allow the user to enter the quantity received and any notes.
4.  This will create a new `StockEntry` document with `type: "intake"`.

#### c. Stock Counting

1.  The "Counting" screen will allow the user to start a new "stock count session."
2.  The user will go through the inventory, scanning each product's barcode.
3.  For each scan, the app will increment a "counted" quantity.
4.  At the end of the session, the app will show a summary of discrepancies between the "counted" stock and the "expected" stock.
5.  The user can then choose to create `StockEntry` documents (`type: "adjustment"`) to correct the stock levels.

---

### 5. Full-Text Search

*   A prominent search bar will be available on the "Products" and "Sell" screens.
*   As the user types, the search results will update in real-time.
*   The search will match on product name, description, and SKU.
*   The search will be performed entirely on the client-side for offline functionality.

This UI/UX approach ensures that the application is intuitive, efficient, and meets all the specified functional requirements, with a strong emphasis on the offline, picture-centric, and keyboard-friendly aspects of the design.
