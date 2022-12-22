<script>
export default {
    data() {
        return {
            count: 0
        }
    },
    methods: {
        increaseCount() {
            this.count++
        },
        decreaseCount() {
            if (this.count > 0) {
                this.count--
            }
        }
    }
}
</script>
<template>
    <div class="input-group input-group-sm">
        <button class="btn btn-secondary" type="button" @click="increaseCount">+</button>
        <input type="number" class="form-control text-center" v-model="count">
        <button class="btn btn-secondary" type="button" @click="decreaseCount">-</button>
    </div>
</template>