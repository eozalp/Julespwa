<template>
  <div class="insights">
    <h1>Insights</h1>
    <div class="controls">
      <sort-options @sort-change="onSortChange" />
      <filter-options @filter-change="onFilterChange" />
    </div>
    <div class="product-grid">
      <product-card
        v-for="product in displayedProducts"
        :key="product._id"
        :product="product"
      />
    </div>
  </div>
</template>

<script>
// import ProductCard from '@/components/ProductCard.vue';
// import SortOptions from '@/components/SortOptions.vue';
// import FilterOptions from '@/components/FilterOptions.vue';
// import analyticsService from '@/services/analyticsService';

export default {
  name: 'InsightsView',
  // components: { ProductCard, SortOptions, FilterOptions },
  data() {
    return {
      productsWithPerformance: [],
      sortOption: 'best-selling',
      filterOptions: {},
    };
  },
  computed: {
    displayedProducts() {
      // In a real implementation, this would contain the sorted and filtered logic
      return this.productsWithPerformance;
    },
  },
  methods: {
    onSortChange(newSortOption) {
      this.sortOption = newSortOption;
    },
    onFilterChange(newFilterOptions) {
      this.filterOptions = newFilterOptions;
    },
    async loadInsights() {
      // this.productsWithPerformance = await analyticsService.getProductsWithPerformance();
      console.log('Loading insights data...');
    },
  },
  created() {
    this.loadInsights();
  },
};
</script>

<style scoped>
.controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
</style>
