<script>
import invoice from '../components/invoice.vue'
import displayProduct from '../components/displayProduct.vue';


export default {
    components: { invoice, displayProduct },
    methods: {
        gotoReportSale() {
            this.$router.push({
                path: "/reportSale"
            })
        },
    }
}
</script>

<template>
    <!-- title -->
    <div class="text-center mt-5 text-light">
        <h1>Simple Point of Sale</h1>
    </div>


    <!-- content -->
    <div class="container-fluid">
        <div class="row" style="height: 720px">
            <!-- invoice and payment stuffs -->
            <invoice></invoice>

            <!-- display and admin command stuffs -->
            <div class="col-9 d-flex flex-column flex-wrap border border-light">
                <!-- display -->
                <displayProduct></displayProduct>

                <!-- admin command -->
                <div class="row m-2" style="height: 45px">
                    <div class="col-12 d-flex justify-content-center">
                        <button type="button" class="btn btn-primary p-2" style="width: 72%;"
                            @click="gotoReportSale">Sale Report</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>