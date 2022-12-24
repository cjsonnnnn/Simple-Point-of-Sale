<script>
import { useInvoiceStore } from '../stores/invoice';
import { useDataStore } from '../stores/data';

export default {
    data() {
        return {
            invoiceStore: {},
            dataStore: {}
        }
    },
    methods: {
        gotoHome() {
            this.$router.push({
                path: '/'
            })
        },

        // temporary
        paymentConfirmation() {
            // update data, transaction
            let transaction = {
                noInvoice: this.invoiceStore.invoiceId,
                product: [],
                grandTotal: this.invoiceStore.grandTotal,
                date: this.invoiceStore.date,
            }
            // get products from cart
            for (let i = 0; i < this.invoiceStore.cart.length; i++) {
                transaction.product.push(this.invoiceStore.cart[i].product_id)
            }
            this.dataStore.transaction.push(transaction)
            console.log(this.dataStore.transaction)

            // reset invoice
            this.invoiceStore.resetInvoice()

            // back to home page
            this.gotoHome()
        }
    },
    created() {
        this.invoiceStore = useInvoiceStore(),
            this.dataStore = useDataStore()
    }
}
</script>
<template>
    <!-- title -->
    <div class="text-center mt-5">
        <h1>Payment</h1>
    </div>

    <div class="bg-secondary" style="height: 774px">
        <!-- table container -->
        <div class="container-fluid bg-warning overflow-auto" style="height: 630px">
            <table class="table text-white table-hover">
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
                    <tr v-for="(product, index) in invoiceStore.cart">
                        <th scope="row">{{ index + 1 }}</th>
                        <td>{{ product.name }}</td>
                        <td>{{ product.qty }}</td>
                        <td>{{ invoiceStore.rpFormat(product.price) }}</td>
                        <td>{{ invoiceStore.rpFormat(product.subTotal) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- summarizes -->
        <div class="container-fluid">
            <div class="row bg-primary justify-content-end">
                <div class="col-4 p-0">
                    <div class="container-fluid bg-success">
                        <!-- total -->
                        <div class="row">
                            <div class="col-4 bg-danger p-2">
                                Total
                            </div>
                            <div class="col-8 bg-danger p-2">
                                : {{ invoiceStore.rpFormat(invoiceStore.total) }}
                            </div>
                        </div>

                        <!-- discount -->
                        <div class="row">
                            <div class="col-4 bg-danger p-2">
                                Diskon
                            </div>
                            <div class="col-8 bg-danger p-2">
                                : {{ invoiceStore.discountFormat }}
                            </div>
                        </div>

                        <!-- grand total -->
                        <div class="row">
                            <div class="col-4 bg-danger p-2">
                                Grand Total
                            </div>
                            <div class="col-8 bg-danger p-2">
                                : {{ invoiceStore.rpFormat(invoiceStore.grandTotal) }}
                            </div>
                        </div>

                        <!-- confirm payment -->
                        <div class="row bg-warning">
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