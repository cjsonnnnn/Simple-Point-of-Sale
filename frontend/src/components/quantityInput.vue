<script>
import { useInvoiceStore } from '../stores/invoice.js'

export default {
    props: ["pId", "pIndex"],
    data() {
        return {
            invoiceStore: {}
        }
    },
    methods: {
        increaseCount() {
            let pCart = this.invoiceStore.cart.find(x => x.product_id === this.pId)
            // increase qty
            pCart.qty++
            // update subTotal
            this.updateSubtotal
        },
        decreaseCount() {
            let pCart = this.invoiceStore.cart.find(x => x.product_id === this.pId)
            if (pCart.qty > 1) {
                // decrease qty
                pCart.qty--
                // update subTotal
                this.updateSubtotal
            } else {
                let cart = this.invoiceStore.cart
                cart.splice(cart.findIndex(x => x.product_id === this.pId), 1)
            }
        }
    },
    computed: {
        updateSubtotal() {
            let pCart = this.invoiceStore.cart.find(x => x.product_id === this.pId)
            pCart.subTotal = pCart.price * pCart.qty
        }
    },
    created() {
        this.invoiceStore = useInvoiceStore()
    }
}
</script>
<template>
    <div class="input-group input-group-sm">
        <button class="btn btn-secondary" type="button" @click="increaseCount">+</button>
        <input type="number" class="form-control text-center" v-model="invoiceStore.cart[pIndex].qty">
        <button class="btn btn-secondary" type="button" @click="decreaseCount">-</button>
    </div>
</template>