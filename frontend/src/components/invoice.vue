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
        rpFormat(number) {
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
        }
    },
    computed: {
        updateTotal() {
            let cart = this.invoiceStore.cart
            let total = 0
            for (let i = 0; i < cart.length; i++) {
                total += cart[i].subTotal
            }
            this.invoiceStore.total = total
            return this.invoiceStore.total
        },
        diskonFormat() {
            return (this.invoiceStore.discount * 100).toString() + "%"
        },
        updateGTotal() {
            let total = this.invoiceStore.total
            let discount = this.invoiceStore.discount
            this.invoiceStore.grandTotal = Math.floor(total * (1 - discount))
            return this.invoiceStore.grandTotal
        }
    }
    ,
    created() {
        this.invoiceStore = useInvoiceStore()
    }
}
</script>


<template>
    <!-- left area -->
    <div class="col-3 bg-warning d-flex flex-column flex-wrap">
        <!-- header invoice -->
        <div class="row bg-secondary p-2">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 pt-2">No Invoice</div>
                    <div class="col-8 pt-2">: {{ invoiceStore.noInvoice }}</div>
                </div>
            </div>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4 pt-2 pb-2">Tanggal</div>
                    <div class="col-8 pt-2 pb-2">: {{ invoiceStore.date }}</div>
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
                                    <div class="col-4 p-0 d-flex align-items-center">{{ rpFormat(cart.price) }} x
                                    </div>
                                    <div class="col-5 p-0">
                                        <quantityInput :pId="cart.product_id" :pIndex="index"></quantityInput>
                                    </div>
                                </div>
                            </div>

                            <!-- sub total -->
                            <div style="text-align:end;" class="mt-3"><b>{{ rpFormat(cart.subTotal) }}</b></div>
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
                                    <div class="col-7">: {{ rpFormat(updateTotal) }}</div>
                                </div>
                            </div>

                            <!-- diskon -->
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">Diskon</div>
                                    <div class="col-7">: {{ diskonFormat }}</div>
                                </div>
                            </div>

                            <!-- grand total -->
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-5">Grand Total</div>
                                    <div class="col-7">: {{ rpFormat(updateGTotal) }}</div>
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
                <button type="button" class="btn btn-primary p-2" style="width: 72%">Primary</button>
            </div>
        </div>
    </div>
</template>