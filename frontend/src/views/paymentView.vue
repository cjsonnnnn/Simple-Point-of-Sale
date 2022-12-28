<script>
import { useDataStore } from '../stores/data';

export default {
    data() {
        return {
            dataStore: {}
        }
    },
    methods: {
        gotoHome() {
            this.$router.push({
                path: '/'
            })
        },

        paymentConfirmation() {
            // update data, invoice
            let invoice = {
                username: "cusA",
                products: this.dataStore.cart.product_association,
                total_qty: this.dataStore.updateTotalQTY,
                total_price: this.dataStore.cart.grand_price,
                date: this.dataStore.cart.date,
            }
            // get product ids from cart
            // for (let i = 0; i < this.dataStore.cart.product_association.length; i++) {
            //     invoice.products.push(this.dataStore.cart.product_association[i])
            // }
            // this.dataStore.invoice.push(invoice)
            // console.log(this.dataStore.invoice)
            this.dataStore.addInvoice(invoice)

            // reset cart
            this.dataStore.resetCart("cusA")

            // back to home page
            this.gotoHome()
        }
    },
    created() {
        this.dataStore = useDataStore()
        this.dataStore.getProducts()
        this.dataStore.getCart("cusA")
    }
}
</script>
<template>
    <!-- title -->
    <div class="text-center mt-5 text-light">
        <h1>Payment</h1>
    </div>

    <div style="height: 774px">
        <!-- table container -->
        <div class="container-fluid overflow-auto" style="height: 630px">
            <table class="table text-white">
                <thead class="table-light text-center">
                    <tr>
                        <th scope="col" style="width: 54px">No</th>
                        <th scope="col">Product</th>
                        <th scope="col">Qty</th>
                        <th scope="col">Price</th>
                        <th scope="col">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(product, index) in dataStore.cart.product_association">
                        <th scope="row">{{ index + 1 }}</th>
                        <td>{{ dataStore.product[index].name }}</td>
                        <td>{{ product.qty }}</td>
                        <td>{{ dataStore.rpFormat(dataStore.product[index].price) }}</td>
                        <td>{{ dataStore.rpFormat(product.subtotal) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- summarizes -->
        <div class="container-fluid ">
            <div class="row justify-content-end">
                <div class="col-4 p-2 border border-light">
                    <div class="container-fluid text-light">
                        <!-- total -->
                        <div class="row">
                            <div class="col-4 p-2">
                                Total
                            </div>
                            <div class="col-8 p-2">
                                : {{ dataStore.rpFormat(dataStore.cart.price) }}
                            </div>
                        </div>

                        <!-- discount -->
                        <div class="row">
                            <div class="col-4 p-2">
                                Discount
                            </div>
                            <div class="col-8 p-2">
                                : {{ dataStore.discountFormat }}
                            </div>
                        </div>

                        <!-- grand total -->
                        <div class="row">
                            <div class="col-4 p-2">
                                Grand Total
                            </div>
                            <div class="col-8 p-2">
                                : {{ dataStore.rpFormat(dataStore.cart.grand_price) }}
                            </div>
                        </div>

                        <!-- confirm payment -->
                        <div class="row">
                            <button type="button" class="btn btn-success col-12 p-2 mt-2" data-bs-toggle="modal"
                                data-bs-target="#payconf">Confirm Payment</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>



    <!-- payment confirmation modal -->
    <div class="modal fade" id="payconf" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
        aria-labelledby="payconfLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5 text-black" id="payconfLabel">Payment Confirmation</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body text-black">
                    Are you sure want to proceed?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-success ps-4 pe-4" @click="paymentConfirmation"
                        data-bs-dismiss="modal">Pay</button>
                    <span id="yourtargetiddelete" style="display: none;"></span>
                </div>
            </div>
        </div>
    </div>
</template>