<script>
import { useCustomerStore } from '../stores/customer';
import { useDataStore } from '../stores/data';
import quantityInput from './quantityInput.vue';

export default {
    components: { quantityInput },
    data() {
        return {
            dataStore: {},
            customerStore: {},
            cartedProducts: []
        }
    },
    methods: {
        gotoPayment() {
            this.dataStore.updateCart()

            this.$router.push({
                path: "/payment"
            })
        },
        loginCustomer() {
            let usernameElement = document.getElementById("customerUsername")
            let passwordElement = document.getElementById("customerPassword")

            // send data to store
            let dataLogin = {
                "username": usernameElement.value,
                "password": passwordElement.value
            }
            this.customerStore.login(dataLogin)

            // update form appearances
            usernameElement.value = ""
            passwordElement.value = ""
        }
    },
    computed: {
        getCartedProducts() {
            // get all ids
            let pIds = []
            for (let i = 0; i < this.dataStore.cart.product_association.length; i++) {
                pIds.push(this.dataStore.cart.product_association[i].product_id)
            }

            // get product details
            let cartedProducts = []
            for (let i = 0; i < pIds.length; i++) {
                cartedProducts.push(this.dataStore.product[this.dataStore.product.findIndex(x => x.id === pIds[i])])
            }
            this.cartedProducts = cartedProducts
            // console.log(this.cartedProducts)
            // console.log(this.cartedProducts[0])
            return this.cartedProducts
        }
    },
    created() {
        this.dataStore = useDataStore()
        this.customerStore = useCustomerStore()

        // re-verify whether or not a user is logged in
        this.customerStore.getSession()
    }
}
</script>


<template>
    <div>{{ this.customerStore.csrfToken }}</div>
    <div>{{ this.customerStore.isAuthenticated }}</div>
    <!-- invoice and payment stuffs -->
    <div class="col-3 d-flex flex-column flex-wrap border border-light">
        <!-- header invoice -->
        <div class="row p-2 text-light border border-light" v-if="this.customerStore.isAuthenticated">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 pt-2">Cart ID</div>
                    <div class="col-8 pt-2">: {{ dataStore.cart.id }}</div>
                </div>
            </div>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 pt-2 pb-2">Date</div>
                    <div class="col-8 pt-2 pb-2">: {{ dataStore.updateDate }}</div>
                </div>
            </div>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 pb-2">Username</div>
                    <div class="col-8 pb-2">: {{ dataStore.cart.username }}</div>
                    <button type="button" class="btn btn-outline-light me-1" @click="this.customerStore.logout()"
                        style="flex: 1 1 0px">
                        Logout
                    </button>
                </div>
            </div>
        </div>
        <div class="row p-2 text-light border border-light" v-else>
            <div class="container-fluid">
                <div class="row">
                    <input type="text" placeholder="input your username here" id="customerUsername" class="mb-3">
                    <input type="password" placeholder="input your password here" id="customerPassword" class="mb-3">
                    <div class="d-flex flex-row flex-wrap justify-content-between">
                        <button type="button" class="btn btn-outline-light me-1" @click="" style="flex: 1 1 0px">Sign
                            Up</button>
                        <button type="button" class="btn btn-outline-light ms-1" @click="this.loginCustomer()"
                            style="flex: 1 1 0px">
                            Login
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- invoice body -->
        <div class="row d-flex flex-fill">
            <!-- invoice products -->
            <div class="row m-0 overflow-auto" style="height: 481px">
                <div class="container-fluid p-2">
                    <!-- a product -->
                    <div class="row overflow-hidden mt-3 bg-light text-black" style="border-radius: 9px"
                        v-for="(product, index) in getCartedProducts" :key="product.id">
                        <!-- image -->
                        <div class="col-12 p-0" style="height: 110px">
                            <img :src="product.img_link" alt="">
                        </div>

                        <!-- product's descriptions -->
                        <div class="col-12">
                            <!-- item name -->
                            <div>{{ product.name }}</div>

                            <!-- item price and qty -->
                            <div class="container-fluid mt-1">
                                <div class="row p-0">
                                    <div class="col-5 p-0 d-flex align-items-center">
                                        {{ dataStore.rpFormat(product.price) }} x
                                    </div>
                                    <div class="col-5 p-0">
                                        <quantityInput :pId="product.id" :pIndex="index"></quantityInput>
                                    </div>
                                </div>
                            </div>

                            <!-- sub total -->
                            <div style="text-align:end;" class="mt-3">
                                <b>{{ dataStore.rpFormat(dataStore.cart.product_association[index].subtotal) }}</b>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- invoice summaries -->
            <div class="row m-0 d-flex align-items-center justify-content-start m-0 p-0" style="height: 15%">
                <div class="container-fluid text-light">
                    <div class="row justify-content-start">
                        <div class="col-12 ps-0">
                            <!-- total -->
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">Total</div>
                                    <div class="col-7">: {{ dataStore.rpFormat(dataStore.updateTotal) }}</div>
                                </div>
                            </div>

                            <!-- diskon -->
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">Diskon</div>
                                    <div class="col-7">: {{ dataStore.discountFormat }}</div>
                                </div>
                            </div>

                            <!-- grand total -->
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">Grand Total</div>
                                    <div class="col-7">: {{ dataStore.rpFormat(dataStore.updateGTotal) }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- commands -->
        <div class="row m-2" style="height: 45px">
            <div class="col-12 d-flex justify-content-center">
                <button type="button" class="btn btn-primary p-2" style="width: 72%" @click="gotoPayment"
                    v-if="dataStore.cart.product_association.length > 0">
                    Proceed Payment
                </button>
                <button type="button" class="btn btn-primary p-2" style="width: 72%" data-bs-toggle="modal"
                    data-bs-target="#alert-empty-cart" v-else>
                    Proceed Payment
                </button>
            </div>
        </div>


        <!-- alert modal -->
        <div class="modal fade" tabindex="-1" id="alert-empty-cart">
            <div class="modal-dialog">
                <div class="modal-content text-black">
                    <div class="modal-header">
                        <h5 class="modal-title">Alert</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p>Please fill the cart</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* style for form login */
#customerUsername,
#customerPassword {
    background: transparent;
    border: none;
    color: white;
    border-bottom: 1px solid white;
}

#customerUsername:focus,
#customerPassword:focus {
    outline: none;
}

#customerUsername::placeholder,
#customerPassword::placeholder {
    color: #dfdfdf
}
</style>