<template>
  <div class="counting">
    <h1>Stock Counting</h1>
    <barcode-scanner @barcode-scanned="onBarcodeScanned" />
    <div class="counts">
      <h2>Counts</h2>
      <ul>
        <li v-for="(count, barcode) in counts" :key="barcode">
          {{ barcode }}: {{ count }}
        </li>
      </ul>
      <button @click="finishCount">Finish Count</button>
    </div>
  </div>
</template>

<script>
// import BarcodeScanner from '@/components/BarcodeScanner.vue';
// import db from '@/db';

export default {
  name: 'CountingView',
  // components: { BarcodeScanner },
  data() {
    return {
      counts: {},
    };
  },
  methods: {
    onBarcodeScanned(barcode) {
      if (this.counts[barcode]) {
        this.counts[barcode]++;
      } else {
        this.counts[barcode] = 1;
      }
    },
    async finishCount() {
      // for (const barcode in this.counts) {
      //   const product = await db.products.where('sku').equals(barcode).first();
      //   if (product) {
      //     const adjustment = this.counts[barcode] - product.stock;
      //     if (adjustment !== 0) {
      //       await db.stockEntries.add({
      //         productId: product._id,
      //         type: 'adjustment',
      //         quantity: adjustment,
      //         createdAt: new Date(),
      //       });
      //       await db.products.update(product._id, { stock: this.counts[barcode] });
      //     }
      //   }
      // }
      console.log('Count finished:', this.counts);
      this.counts = {};
    },
  },
};
</script>
