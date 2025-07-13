<template>
  <div class="product-card">
    <img :src="heroImage" :alt="product.name" class="product-image" />
    <div class="product-info">
      <h3>{{ product.name }}</h3>
      <div class="performance-metrics">
        <p><strong>Units Sold:</strong> {{ product.unitsSold || 0 }}</p>
        <p><strong>Revenue:</strong> ${{ (product.totalRevenue || 0).toFixed(2) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  computed: {
    heroImage() {
      if (this.product.pictures && this.product.pictures.length > 0) {
        return this.product.pictures[0];
      }
      // Return a placeholder image if no pictures are available
      return 'https://via.placeholder.com/250';
    },
  },
};
</script>

<style scoped>
.product-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.product-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}
.product-info {
  padding: 1rem;
}
.performance-metrics {
  margin-top: 0.5rem;
  font-size: 0.9rem;
}
</style>
