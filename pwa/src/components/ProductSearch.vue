<template>
  <div class="product-search">
    <input type="text" v-model="query" @input="search" placeholder="Search for products..." />
    <ul>
      <li v-for="product in results" :key="product._id" @click="addProduct(product)">
        {{ product.name }}
      </li>
    </ul>
  </div>
</template>

<script>
// import searchService from '@/services/searchService';

export default {
  name: 'ProductSearch',
  data() {
    return {
      query: '',
      results: [],
    };
  },
  methods: {
    async search() {
      // this.results = await searchService.search(this.query);
      console.log('Searching for:', this.query);
    },
    addProduct(product) {
      this.$emit('add-to-cart', product);
    },
  },
};
</script>
