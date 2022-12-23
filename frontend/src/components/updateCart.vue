<script>
import axios from "axios"
import { useDataStore } from '../stores/data.js'
import { useInvoiceStore } from '../stores/invoice.js'

export default {
    props: ["pId"],
    data() {
        return {
            invoiceStore: {},
            dataStore: {}
        }
    },
    methods: {
        // getData() {
        //     console.log(axios({
        //         method: 'post',
        //         url: 'http://localhost:5000/addP',
        //         data: this.product[0]
        //     }).then(res => {
        //         console.log("got it");
        //         console.log(res);
        //     }).catch(err => {
        //         console.log("error")
        //         console.log(err);
        //     }))
        // }
        // getData() {
        //     console.log(axios.get('http://localhost:5000/getProduct')
        //         .then(res => {
        //             console.log("got it");
        //             console.log(res);
        //         }).catch(err => {
        //             console.log("error")
        //             console.log(err);
        //         }))
        // }
        addCart() {
            // add a product to cart
            let product = this.dataStore.product.find(x => x.product_id === this.pId)
            let pCart = {
                product_id: product.product_id,
                name: product.name,
                price: product.price,
                qty: 1,
                subTotal: product.price,
                imgLink: product.imgLink,
            }
            this.invoiceStore.cart.push(pCart)
        },
        removeCart() {
            // remove a product from cart
            let cart = this.invoiceStore.cart
            let index = cart.findIndex(x => x.product_id === this.pId)

            // to avoid removing object from index -1 or under
            if (index > -1) {
                cart.splice(index, 1)
            }
        }
    },
    computed: {
        isCarted() {
            let isInCart = this.invoiceStore.cart.find(x => x.product_id === this.pId)
            return isInCart
        }
    },
    created() {
        this.dataStore = useDataStore(),
            this.invoiceStore = useInvoiceStore()
    }
}
</script>
<template>
    <button type="button" class="btn btn-danger ps-4 pe-4" @click="removeCart" v-if="isCarted">Cancel</button>
    <button type="button" class="btn btn-primary ps-4 pe-4" @click="addCart" v-else="isCarted">Add</button>
</template>