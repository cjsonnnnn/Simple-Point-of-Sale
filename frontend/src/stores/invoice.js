import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useInvoiceStore = defineStore('invoice', {
  state: () => ({
    noInvoice: "08954322",
    date: "17/09/22",
    username: "jsonnnnn___",
    cart: [],
    total: 4312424,
    discount: 0.3,
    grandTotal: 70000
  }),
})
