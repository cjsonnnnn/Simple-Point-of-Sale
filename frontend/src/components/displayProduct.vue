<script>
import { useDataStore } from '../stores/data.js'
import quantityInput from './quantityInput.vue';
import updateCart from './updateCart.vue';
import invoice from './invoice.vue'

export default {
    components: { quantityInput, invoice, updateCart },
    data() {
        return {
            dataStore: {},
            searchIds: ""
        }
    },
    methods: {
        changeCategory(categoryName) {
            if (categoryName == "all") {
                this.searchIds = ""
            } else {
                this.searchIds = categoryName
            }
        },
        // getData() {
        //     console.log(axios({
        //         method: 'post',
        //         url: 'http://localhost:5000/addP',
        //         data: this.product[0]
        //     }).then(res => {
        //         console.log("got it");
        //         console.log(res);
        //     }).catch(err => {
        //         console.log("error")
        //         console.log(err);
        //     }))
        // }
        // getData() {
        //     console.log(axios.get('http://localhost:5000/getProduct')
        //         .then(res => {
        //             console.log("got it");
        //             console.log(res);
        //         }).catch(err => {
        //             console.log("error")
        //             console.log(err);
        //         }))
        // }
    },
    computed: {
        filteredProduct() {
            return this.dataStore.product.filter(product => {
                if (this.searchIds == "") {
                    return true
                } else {
                    return product.category.includes(this.searchIds)
                }
            })
        }
    },
    created() {
        this.dataStore = useDataStore()
    }
}

</script>
<template>
    <!-- categories -->
    <div class="row bg-success text-center overflow-auto">
        <button type="button" class="btn btn-danger m-2 p-2" style="width: 90px;"
            @click="changeCategory(ctg.toLowerCase())" v-for="ctg in dataStore.category">
            {{ ctg }}
        </button>
    </div>

    <!-- products -->
    <div class="row bg-danger flex-fill">
        <div class="container-fluid overflow-auto" style="height: 630px">
            <div class="row overflow-auto">
                <!-- a product -->
                <div class="col-3 p-2" v-for="product in filteredProduct">
                    <div class="card" style="width: 100%;">
                        <img :src="product.imgLink" class="card-img-top" alt="...">
                        <div class="card-body">
                            <!-- item name -->
                            <div>{{ product.name }}</div>

                            <!-- item price and qty -->
                            <div class="container-fluid mt-1">
                                <div class="row p-0 d-flex flex-column align-items-end">
                                    <!-- price -->
                                    <div class="col-12 p-0 d-flex align-items-center">{{
                                            dataStore.rpFormat(product.price)
                                    }}
                                    </div>

                                    <!-- update cart -->
                                    <div class="col-7 p-0 mt-2 d-flex justify-content-end">
                                        <updateCart :pId="product.product_id"></updateCart>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


    </div>
</template>