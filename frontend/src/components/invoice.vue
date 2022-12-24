<script>
import { useInvoiceStore } from '../stores/invoice.js'
import quantityInput from './quantityInput.vue';

export default {
    components: { quantityInput },
    data() {
        return {
            invoiceStore: {}
        }
    },
    methods: {
        gotoPayment() {
            this.$router.push({
                path: "/payment"
            })
        }
    },
    created() {
        this.invoiceStore = useInvoiceStore()
    }
}
</script>


<template>
    <!-- invoice and payment stuffs -->
    <div class="col-3 bg-warning d-flex flex-column flex-wrap">
        <!-- header invoice -->
        <div class="row bg-secondary p-2">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 pt-2">No Invoice</div>
                    <div class="col-8 pt-2">: {{ invoiceStore.updateInvoiceId }}</div>
                </div>
            </div>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 pt-2 pb-2">Date</div>
                    <div class="col-8 pt-2 pb-2">: {{ invoiceStore.updateDate }}</div>
                </div>
            </div>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 pb-2">Username</div>
                    <div class="col-8 pb-2">: {{ invoiceStore.username }}</div>
                </div>
            </div>
        </div>

        <!-- invoice body -->
        <div class="row bg-success d-flex flex-fill">
            <!-- invoice products -->
            <div class="row bg-warning m-0 overflow-auto" style="height: 481px">
                <div class="container-fluid p-2">
                    <!-- a product -->
                    <div class="row overflow-hidden mt-3" style="border-radius: 9px"
                        v-for="(cart, index) in invoiceStore.cart">
                        <!-- image -->
                        <div class="col-12 bg-danger p-0" style="height: 110px">
                            <img :src="cart.imgLink" alt="">
                        </div>

                        <!-- product's descriptions -->
                        <div class="col-12 bg-primary">
                            <!-- item name -->
                            <div>{{ cart.name }}</div>

                            <!-- item price and qty -->
                            <div class="container-fluid mt-1">
                                <div class="row p-0">
                                    <div class="col-4 p-0 d-flex align-items-center">{{
                                            invoiceStore.rpFormat(cart.price)
                                    }} x
                                    </div>
                                    <div class="col-5 p-0">
                                        <quantityInput :pId="cart.product_id" :pIndex="index"></quantityInput>
                                    </div>
                                </div>
                            </div>

                            <!-- sub total -->
                            <div style="text-align:end;" class="mt-3"><b>{{ invoiceStore.rpFormat(cart.subTotal) }}</b>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- invoice summaries -->
            <div class="row bg-primary m-0 d-flex align-items-center justify-content-start m-0 p-0" style="height: 15%">
                <div class="container-fluid">
                    <div class="row bg-danger justify-content-start">
                        <div class="col-12 ps-0">
                            <!-- total -->
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">Total</div>
                                    <div class="col-7">: {{ invoiceStore.rpFormat(invoiceStore.updateTotal) }}</div>
                                </div>
                            </div>

                            <!-- diskon -->
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">Diskon</div>
                                    <div class="col-7">: {{ invoiceStore.discountFormat }}</div>
                                </div>
                            </div>

                            <!-- grand total -->
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">Grand Total</div>
                                    <div class="col-7">: {{ invoiceStore.rpFormat(invoiceStore.updateGTotal) }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- commands -->
        <div class="row m-2" style="height: 45px">
            <div class="col-12 d-flex justify-content-center bg-danger">
                <button type="button" class="btn btn-primary p-2" style="width: 72%" @click="gotoPayment">
                    Primary
                </button>
            </div>
        </div>
    </div>
</template>