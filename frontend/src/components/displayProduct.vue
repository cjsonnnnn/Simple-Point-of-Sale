<script>
import { useDataStore } from '../stores/data.js'
import updateCart from './updateCart.vue';

export default {
    components: { updateCart },
    data() {
        return {
            dataStore: {},
            searchIds: "",
        }
    },
    methods: {
        changeCategory(categoryName) {
            if (categoryName == "all") {
                this.searchIds = ""
            } else {
                this.searchIds = categoryName
            }
        }
    },
    computed: {
        filteredProduct() {
            return this.dataStore.product.filter(product => {
                if (this.searchIds == "") {
                    return true
                } else {
                    let categories = []
                    for (let i = 0; i < product.categories.length; i++) {
                        categories.push(product.categories[i].name.toLowerCase())
                    }
                    return categories.includes(this.searchIds)
                }
            })
        }
    },
    created() {
        this.dataStore = useDataStore()
        this.dataStore.getProducts()
        this.dataStore.getAllCategories()
        this.dataStore.getCart("cusA")
        this.dataStore.getInvoice("cusA")
    }
}

</script>
<template>
    <!-- categories -->
    <div class="row text-center overflow-auto border border-light">
        <button type="button" class="btn btn-light m-2 p-2" style="width: 126px;"
            @click="changeCategory(ctg.toLowerCase())" v-for="ctg in dataStore.category">
            {{ ctg }}
        </button>
    </div>

    <!-- products -->
    <div class="row flex-fill border border-light">
        <div class="container-fluid overflow-auto" style="height: 630px">
            <div class="row overflow-auto">
                <!-- a product -->
                <div class="col-3 p-2" v-for="product in filteredProduct">
                    <div class="card" style="width: 100%;">
                        <img :src="product.img_link" class="card-img-top" alt="...">
                        <div class="card-body text-black">
                            <!-- item name -->
                            <div>{{ product.name }}</div>

                            <!-- item price and qty -->
                            <div class="container-fluid mt-1">
                                <div class="row p-0 d-flex flex-column align-items-end">
                                    <!-- price -->
                                    <div class="col-12 p-0 d-flex align-items-center">
                                        {{ dataStore.rpFormat(product.price) }}
                                    </div>

                                    <!-- update cart -->
                                    <div class="col-7 p-0 mt-2 d-flex justify-content-end">
                                        <updateCart :pId="product.id"></updateCart>
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