import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useInvoiceStore = defineStore('invoice', {
  state: () => ({
    noInvoice: "08954322",
    date: "17/09/22",
    username: "jsonnnnn___",
    cart: [
      {
        id: "p-1",
        name: "Kamera 1",
        price: 30000,
        qty: 3,
        subTotal: 90000
      }
    ],
    total: 100000,
    diskon: 0.3,
    grandTotal: 70000
  })
})
