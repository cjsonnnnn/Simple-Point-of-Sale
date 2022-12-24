<script>
import { useDataStore } from '../stores/data';

export default {
    data() {
        return {
            dataStore: {}
        }
    },
    methods: {
        jaj() {
            console.log("hei")
        }
    },
    created() {
        this.dataStore = useDataStore()
    }
}
</script>

<template>
    <!-- title -->
    <div class="text-center mt-5">
        <h1>Report Sale</h1>
    </div>

    <!-- table container -->
    <div class="container-fluid bg-warning overflow-auto" style="height: 774px">
        <table class="table text-white table-hover">
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
                <tr v-for="(inv, index) in dataStore.transaction">
                    <th scope="row">{{ index + 1 }}</th>
                    <td>{{ inv.date }}</td>
                    <td>{{ inv.invoiceId }}</td>
                    <td>{{ inv.username }}</td>
                    <td>{{ inv.product.length }}</td>
                    <td>{{ dataStore.rpFormat(inv.total) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>