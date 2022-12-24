import { createRouter, createWebHistory } from 'vue-router'
import homeView from '../views/homeView.vue'
import reportView from '../views/reportView.vue'
import paymentView from '../views/paymentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: homeView
    },
    {
      path: "/reportSale",
      name: "reportsale",
      component: reportView
    },
    {
      path: "/payment",
      name: "payment",
      component: paymentView
    }
  ]
})

export default router
