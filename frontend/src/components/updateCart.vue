<script>
import { useDataStore } from '../stores/data.js'

export default {
    props: ["pId"],
    data() {
        return {
            dataStore: {}
        }
    },
    methods: {
        addCartProduct() {
            // add a product to cart
            this.dataStore.addCartProduct("cusA", this.pId)
        },
        cancelCartProduct() {
            // // remove a product from cart
            this.dataStore.removeCartProduct("cusA", this.pId)
        }
    },
    computed: {
        isCarted() {
            let cartProducts = []
            for (let i = 0; i < this.dataStore.cart.product_association.length; i++) {
                cartProducts.push(this.dataStore.cart.product_association[i])
            }
            return cartProducts.find(x => x.product_id === this.pId)
        }
    },
    created() {
        this.dataStore = useDataStore()
    }
}
</script>
<template>
    <button type="button" class="btn btn-danger ps-4 pe-4" @click="cancelCartProduct" v-if="isCarted">Cancel</button>
    <button type="button" class="btn btn-primary ps-4 pe-4" @click="addCartProduct" v-else>Add</button>
</template>