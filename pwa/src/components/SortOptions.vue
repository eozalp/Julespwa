<template>
  <div class="sort-options">
    <label for="sort">Sort by:</label>
    <select id="sort" v-model="selectedSort" @change="emitSortChange">
      <option value="best-selling">Best Selling</option>
      <option value="highest-revenue">Highest Revenue</option>
      <option value="most-recent">Most Recently Sold</option>
      <option value="stock-desc">Stock (High to Low)</option>
      <option value="stock-asc">Stock (Low to High)</option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'SortOptions',
  data() {
    return {
      selectedSort: 'best-selling',
    };
  },
  methods: {
    emitSortChange() {
      this.$emit('sort-change', this.selectedSort);
    },
  },
};
</script>

<style scoped>
.sort-options {
  display: flex;
  align-items: center;
}
label {
  margin-right: 0.5rem;
}
</style>
