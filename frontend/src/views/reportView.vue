<script>
import { useDataStore } from '../stores/data';

export default {
    data() {
        return {
            dataStore: {},
        }
    },
    methods: {
        gotoHome() {
            this.$router.push({
                path: '/'
            })
        },
    },
    computed: {
        getInvoices() {
            console.log("ANJAY")
            console.log(this.dataStore.invoice)
            return this.dataStore.invoice
        }
    },
    created() {
        this.dataStore = useDataStore()
        this.dataStore.getInvoice("cusA")
        // console.log(this.dataStore.invoice)
        // console.log(this.dataStore.invoice[0])
        // console.log("DASD")
    }
}
</script>

<template>
    <!-- title -->
    <div class="text-center mt-5 text-light">
        <h1>Report Sale</h1>
    </div>

    <!-- table container -->
    <div class="container-fluid overflow-auto" style="height: 774px">
        <table class="table text-white">
            <thead class="table-light">
                <tr>
                    <th scope="col" style="width: 54px">No</th>
                    <th scope="col">Date</th>
                    <th scope="col">Invoice Id</th>
                    <th scope="col">Customer</th>
                    <th scope="col">Qty</th>
                    <th scope="col">Total</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(invoice, index) in getInvoices">
                    <th scope="row">{{ index + 1 }}</th>
                    <td>{{ invoice.date }}</td>
                    <td>{{ invoice.id }}</td>
                    <td>{{ invoice.username }}</td>
                    <td>{{ invoice.total_qty }}</td>
                    <td>{{ dataStore.rpFormat(invoice.total_price) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>