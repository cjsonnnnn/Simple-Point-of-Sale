import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useDataStore = defineStore('data', {
    state: () => ({
        product: [
            {
                product_id: "p1",
                name: "Kamera 1",
                price: 20000,
                category: ["handphone", "iphone"],
                imgLink: "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=300"
            },
            {
                product_id: "p2",
                name: "Kamera 2",
                price: 200000,
                category: ["kamera"],
                imgLink: "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=300"
            }
        ],
        transaction: [
            {
            }
        ],
        category: [
            "All",
            "Kamera"
        ]
    }),
})


// category as a list