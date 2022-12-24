import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useInvoiceStore = defineStore('invoice', {
  state: () => ({
    invoiceId: "",
    date: "",
    username: "jsonnnnn___",
    cart: [],
    total: 0,
    discount: 0.3,
    grandTotal: 0
  }),

  actions: {
    // untechnical stuffs
    rpFormat(number) {
      let strNumber = (number).toString()
      let strLength = strNumber.length
      let loopNumber = Math.floor(strLength / 3)
      let rupiah = "Rp. "
      for (let i = 0; i < loopNumber; i++) {
        let front = strNumber.substring(0, strLength - (3 * (i + 1) + i))
        let back = strNumber.substring(strLength - (3 * (i + 1) + i), strLength)
        if (front) {
          strNumber = front + "," + back
        }
        strLength = strNumber.length
      }
      return rupiah.concat(strNumber)
    },

    // technical stuffs
    resetInvoice() {
      this.invoiceId = this.updateInvoiceId
      this.date = this.updateDate
      this.cart = []
      this.total = 0
      this.grandTotal = 0
    }
  },

  getters: {
    // untechnical stuffs
    discountFormat() {
      return (this.discount * 100).toString() + "%"
    },

    // technical stuffs
    updateInvoiceId() {
      let date = new Date()
      date = `${date.getDate()}${date.getMonth() + 1}${date.getFullYear()}${date.getHours()}`
      let invoiceId = "inv-".concat(date)
      // update
      this.invoiceId = invoiceId
      return this.invoiceId
    },
    updateDate() {
      let date = new Date()
      date = `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`
      // update
      this.date = date
      return this.date
    },
    updateTotal() {
      let cart = this.cart
      let total = 0
      for (let i = 0; i < cart.length; i++) {
        total += cart[i].subTotal
      }
      // update
      this.total = total
      return this.total
    },
    updateGTotal() {
      let total = this.total
      let discount = this.discount
      // update
      this.grandTotal = Math.floor(total * (1 - discount))
      return this.grandTotal
    }
  },

  created() {
  }
})
