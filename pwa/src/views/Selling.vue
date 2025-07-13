<template>
  <div class="selling">
    <h1>Selling</h1>
    <product-search @add-to-cart="addToCart" />
    <div class="cart">
      <h2>Cart</h2>
      <ul>
        <li v-for="item in cart" :key="item.productId">
          {{ item.name }} - {{ item.quantity }} x ${{ item.price }}
        </li>
      </ul>
      <p>Total: ${{ total }}</p>
      <button @click="checkout">Checkout</button>
    </div>
  </div>
</template>

<script>
// import ProductSearch from '@/components/ProductSearch.vue';
// import db from '@/db';

export default {
  name: 'SellingView',
  // components: { ProductSearch },
  data() {
    return {
      cart: [],
    };
  },
  computed: {
    total() {
      return this.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    },
  },
  methods: {
    addToCart(product) {
      const cartItem = this.cart.find(item => item.productId === product._id);
      if (cartItem) {
        cartItem.quantity++;
      } else {
        this.cart.push({
          productId: product._id,
          name: product.name,
          price: product.price,
          quantity: 1,
        });
      }
    },
    async checkout() {
      // await db.sales.add({
      //   items: this.cart,
      //   total: this.total,
      //   createdAt: new Date(),
      // });
      console.log('Checkout complete:', this.cart);
      this.cart = [];
    },
  },
};
</script>
