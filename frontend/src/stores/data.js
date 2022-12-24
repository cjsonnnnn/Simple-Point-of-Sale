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
                // noInvoice: "",
                // product: [],
                // grandTotal: "",
                // date: "",
            }
        ],
        category: [
            "All",
            "Kamera"
        ],
    }),

    actions: {
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
    }
})


// category as a list