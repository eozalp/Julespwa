This document outlines the strategy for implementing a fast and efficient batch barcode reading feature.

### 1. The Goal

The goal is to allow the user to continuously scan a series of 1D barcodes (like UPC or EAN) without having to press a button for each scan. This is essential for tasks like stock counting or receiving large shipments, where efficiency is key.

### 2. Core Technology: `BarcodeDetector` API

*   **Primary Choice:** The native `BarcodeDetector` API will be our first choice.
    *   **Why?** Being a native browser API, it is highly optimized for performance and energy efficiency. It offloads the image processing from the JavaScript thread, leading to a smoother UI.
*   **Fallback:** `jsQR`
    *   **Why?** The `BarcodeDetector` API is not yet supported in all browsers (notably Firefox and Safari on iOS). `jsQR` is a lightweight and reliable pure-JavaScript library that can serve as an excellent fallback. We will detect browser support and load `jsQR` only when necessary.

### 3. Implementation Strategy

1.  **UI Component (`BarcodeScanner.vue`):**
    *   This component will contain the `<video>` element to display the camera feed.
    *   It will have a "Start Scanning" button to initialize the camera and a "Stop Scanning" button.
    *   It will display a visual overlay (e.g., a red line or a rectangle) to guide the user on where to position the barcode.

2.  **Camera Access:**
    *   We will use `navigator.mediaDevices.getUserMedia()` to get access to the device's camera.
    *   We will request the rear-facing camera (`{ facingMode: 'environment' }`) as is standard for barcode scanning.

3.  **Continuous Scanning Loop:**
    *   Once the camera stream is active, we will start a continuous scanning loop using `requestAnimationFrame`. This is more efficient than using `setInterval` as it ties into the browser's rendering cycle.
    *   Inside the loop, we will:
        a.  Draw the current frame from the `<video>` element onto a hidden `<canvas>` element.
        b.  Pass the canvas to the `BarcodeDetector.detect()` method (or `jsQR()`).
        c.  If a barcode is detected, we will process it.

4.  **Processing Detected Barcodes:**
    *   To avoid processing the same barcode multiple times per second, we will implement a "debounce" mechanism.
    *   When a barcode is successfully detected and its value is read:
        a.  We will add the barcode's value to a list in the component's state.
        b.  We will provide haptic feedback (if the browser supports it) and/or an audible "beep" to confirm the scan.
        c.  We will briefly pause the scanning loop (e.g., for 500ms) to allow the user to move to the next item.
        d.  The component will emit an event (`barcode-scanned`) with the barcode's value, which the parent component (e.g., `Counting.vue` or `Receiving.vue`) can then handle.

5.  **Batch Handling:**
    *   The parent component will collect the scanned barcode values.
    *   For example, in the "Counting" workflow, the parent component will maintain a dictionary or map where keys are the barcode values and values are the counts.
    *   When a new barcode is scanned, it will increment the count for that barcode.

### 4. Example Code Snippet (Conceptual)

```javascript
// In BarcodeScanner.vue
<template>
  <div>
    <video ref="video" autoplay></video>
    <button @click="startScan">Start Scanning</button>
    <button @click="stopScan">Stop Scanning</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isScanning: false,
      lastScanned: null,
      lastScannedTime: 0,
    };
  },
  methods: {
    async startScan() {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      this.$refs.video.srcObject = stream;
      this.isScanning = true;
      this.scanLoop();
    },
    async scanLoop() {
      if (!this.isScanning) return;

      const barcodeDetector = new BarcodeDetector({ formats: ['ean_13', 'upc_a'] });
      const barcodes = await barcodeDetector.detect(this.$refs.video);

      if (barcodes.length > 0) {
        const barcodeValue = barcodes[0].rawValue;

        // Debounce to avoid multiple scans of the same item
        if (this.lastScanned !== barcodeValue || Date.now() - this.lastScannedTime > 500) {
          this.lastScanned = barcodeValue;
          this.lastScannedTime = Date.now();

          // Vibrate for feedback
          if ('vibrate' in navigator) navigator.vibrate(100);

          this.$emit('barcode-scanned', barcodeValue);
        }
      }

      requestAnimationFrame(this.scanLoop);
    },
    stopScan() {
      this.isScanning = false;
      this.$refs.video.srcObject.getTracks().forEach(track => track.stop());
    }
  }
};
</script>
```

This strategy provides a robust and user-friendly batch barcode scanning experience, leveraging modern browser APIs for performance while ensuring a fallback for wider compatibility.
