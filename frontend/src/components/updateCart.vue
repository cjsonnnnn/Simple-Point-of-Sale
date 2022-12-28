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
            // // remove all item of a product from cart
            // let cart = this.dataStore.cart
            // let index = cart.findIndex(x => x.id === this.pId)

            // // to avoid removing object from index -1 or under
            // if (index > -1) {
            //     cart.splice(index, 1)
            // }
            this.dataStore.removeCartProduct("cusA", this.pId)
        }
    },
    computed: {
        isCarted() {
            // console.log("isCarted")
            let cartProducts = []
            // console.log(this.dataStore.cart.product_association)
            // console.log(this.dataStore.cart.product_association.length)
            for (let i = 0; i < this.dataStore.cart.product_association.length; i++) {
                cartProducts.push(this.dataStore.cart.product_association[i])
            }
            // console.log(cartProducts)
            let a = cartProducts.find(x => x.product_id === this.pId)
            // console.log(a)
            // console.log(" ")
            return a
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