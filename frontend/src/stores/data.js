import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';

export const useDataStore = defineStore('data', {
    state: () => ({
        customer: [],
        product: [],
        invoice: [],
        category: [],
        cart: {
            date: "",
            discount: 0,
            id: "",
            product_association: [],
            price: 0,
            total_qty: 0,
            username: "",
            grand_price: 0
        }
    }),

    actions: {
        // untechnical
        rpFormat(number) {
            // if (!isNaN(number)) {
            //     console.log("not a problem")
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
            // } else {
            //     console.log("a problem")
            //     return "Rp. 0"
            // }
        },


        // technical get
        getDate() {
            let currentDate = new Date()
            currentDate = `${currentDate.getDate()}/${currentDate.getMonth() + 1}/${currentDate.getFullYear()}`
            return currentDate
        },
        getProducts() {
            axios.get('http://localhost:5000/getProducts')
                .then(res => {
                    this.product = res.data
                }).catch(err => {
                    console.log(err);
                })
        },
        getAllCategories() {
            axios.get('http://localhost:5000/getAllCategories')
                .then(res => {
                    this.category = ["All"]
                    for (let i = 0; i < res.data.length; i++) {
                        this.category.push(res.data[i].name)
                    }
                }).catch(err => {
                    console.log(err);
                })
        },
        getCart(username) {
            axios.get(`http://localhost:5000/getCart/${username}`)
                .then(res => {
                    this.cart = res.data[0]
                }).catch(err => {
                    console.log(err)
                })
        },
        addCartProduct(username, pId) {
            axios.get(`http://localhost:5000/addCartProduct/${username}&${pId}`)
                .then(res => {
                    this.getCart("cusA")
                }).catch(err => {
                    console.log(err)
                })
        },
        removeCartProduct(username, pId) {
            axios.get(`http://localhost:5000/removeCartProduct/${username}&${pId}`)
                .then(res => {
                    this.getCart("cusA")
                }).catch(err => {
                    console.log(err)
                })
        },
        updateCart() {
            axios.post('http://localhost:5000/updateCart', this.cart)
                .then(res => {
                    this.getCart("cusA")
                }).catch(err => {
                    console.log(err)
                })
        },
        resetCart(username) {
            axios.get(`http://localhost:5000/resetCart/${username}`)
                .then(res => {
                    // update cart based on username
                    this.getCart("cusA")
                }).catch(err => {
                    console.log(err)
                })
        },
        getInvoice(username) {
            axios.get(`http://localhost:5000/getInvoice/${username}`)
                .then(res => {
                    // console.log("get invoice")
                    // console.log(res)
                    // console.log(res.data)
                    // console.log(" ")
                    this.invoice = res.data
                }).catch(err => {
                    console.log(err)
                })
        },
        addInvoice(invoiceData) {
            axios.post('http://localhost:5000/addInvoice', invoiceData)
                .then(res => {
                    // update invoice
                    this.getInvoice("cusA")
                }).catch(err => {
                    console.log(err)
                })
        }


        // technical post
        // addCart() {
        //     axios.post('http://localhost:5000/addCart', this.cartForm)
        //         .then(res => {
        //             console.log(res)
        //             this.cartForm = {
        //                 date: "",
        //                 total_qty: "",
        //                 discount: "",
        //                 total_price: "",
        //                 username: "",
        //                 products: []
        //             }
        //         }).catch(err => {
        //             console.log(err)
        //         })
        // }
    },

    getters: {
        discountFormat() {
            return (this.cart.discount).toString() + "%"
        },
        updateDate() {
            let date = new Date()
            date = `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`
            // update
            this.cart.date = date
            return this.cart.date
        },
        updateTotal() {
            let cart = this.cart
            let total = 0
            for (let i = 0; i < cart.product_association.length; i++) {
                total += cart.product_association[i].subtotal
            }
            // update 
            this.cart.price = total
            return this.cart.price
        },
        updateGTotal() {
            let total = this.cart.price
            let discount = this.cart.discount / 100
            // update
            this.cart.grand_price = Math.floor(total * (1 - discount))
            return this.cart.grand_price
        },
        updateTotalQTY() {
            let cart = this.cart
            let qty = 0
            for (let i = 0; i < cart.product_association.length; i++) {
                qty += cart.product_association[i].qty
            }
            // update 
            this.cart.total_qty = qty
            return this.cart.total_qty
        }
    }
})


// category as a list