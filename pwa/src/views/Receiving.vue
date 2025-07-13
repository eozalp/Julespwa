<template>
  <div class="receiving">
    <h1>Receiving</h1>
    <p>This is where the user will receive new stock.</p>
    <barcode-scanner @barcode-scanned="onBarcodeScanned" />
    <div v-if="scannedProduct">
      <h2>{{ scannedProduct.name }}</h2>
      <p>Current Stock: {{ scannedProduct.stock }}</p>
      <input type="number" v-model.number="quantity" placeholder="Quantity received" />
      <button @click="receiveStock">Receive Stock</button>
    </div>
  </div>
</template>

<script>
import BarcodeScanner from '@/components/BarcodeScanner.vue';
import db from '@/db';

export default {
  name: 'ReceivingView',
  components: { BarcodeScanner },
  data() {
    return {
      scannedProduct: null,
      quantity: 0,
    };
  },
  methods: {
    async onBarcodeScanned(barcode) {
      const product = await db.products.where('sku').equals(barcode).first();
      if (product) {
        this.scannedProduct = product;
      } else {
        alert(`Product with barcode ${barcode} not found.`);
        this.scannedProduct = null;
      }
    },
    async receiveStock() {
      if (!this.scannedProduct || this.quantity <= 0) {
        alert("Please scan a product and enter a valid quantity.");
        return;
      }

      await db.stockEntries.add({
        productId: this.scannedProduct._id,
        type: 'intake',
        quantity: this.quantity,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });

      await db.products.update(this.scannedProduct._id, {
        stock: this.scannedProduct.stock + this.quantity,
        updatedAt: new Date().toISOString(),
      });

      alert(`${this.quantity} units of ${this.scannedProduct.name} have been received.`);
      this.scannedProduct = null;
      this.quantity = 0;
    },
  },
};
</script>
