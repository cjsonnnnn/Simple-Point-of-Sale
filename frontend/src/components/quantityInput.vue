<script>
import { useDataStore } from '../stores/data'

export default {
    props: ["pId", "pIndex"],
    data() {
        return {
            dataStore: {}
        }
    },
    methods: {
        increaseCount() {
            let pAssoc = this.dataStore.cart.product_association.find(x => x.product_id === this.pId)
            // increase qty
            pAssoc.qty++
            // update subTotal
            this.updateSubtotal
        },
        decreaseCount() {
            let pAssoc = this.dataStore.cart.product_association.find(x => x.product_id === this.pId)
            if (pAssoc.qty > 1) {
                // decrease qty
                pAssoc.qty--
                // update subTotal
                this.updateSubtotal
            } else {
                let cart = this.dataStore.cart
                this.dataStore.removeCartProduct("cusA", this.pId)
            }
        }
    },
    computed: {
        updateSubtotal() {
            let pAssoc = this.dataStore.cart.product_association.find(x => x.product_id === this.pId)
            let theproduct = {
                categories: [],
                id: "",
                img_link: "",
                name: "",
                price: 0
            }
            if (this.dataStore.product.length > 0) {
                theproduct = this.dataStore.product.find(x => x.id === this.pId)
            }
            pAssoc.subtotal = theproduct.price * pAssoc.qty
        }
    },
    created() {
        this.dataStore = useDataStore()
    }
}
</script>
<template>
    <div class="input-group input-group-sm">
        <button class="btn btn-secondary" type="button" @click="decreaseCount">-</button>
        <input type="number" class="form-control text-center" v-model="dataStore.cart.product_association[pIndex].qty">
        <button class="btn btn-secondary" type="button" @click="increaseCount">+</button>
    </div>
</template>