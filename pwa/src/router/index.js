import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/selling',
    name: 'selling',
    component: () => import('../views/Selling.vue')
  },
  {
    path: '/receiving',
    name: 'receiving',
    component: () => import('../views/Receiving.vue')
  },
  {
    path: '/counting',
    name: 'counting',
    component: () => import('../views/Counting.vue')
  },
  {
    path: '/insights',
    name: 'insights',
    component: () => import('../views/Insights.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
