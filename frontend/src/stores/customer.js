import { defineStore } from 'pinia'
import axios from 'axios'

export const useCustomerStore = defineStore('customerStore', {
    state: () => ({
        csrfToken: "",
        isAuthenticated: false,
    }),
    actions: {
        async login(dataLogin) {
            let axiosWithCookies = axios.create({
                withCredentials: true,
                headers: {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.csrfToken
                }
            })
            await axiosWithCookies.post('http://localhost:5000/login', dataLogin)
                .then(res => {
                    if (res.data["status"] == "success") {
                        this.isAuthenticated = true
                        console.log(res)
                    } else {
                        console.log(res)
                    }
                }).catch(err => {
                    console.log(err)
                })
        },
        async logout() {
            let axiosWithCookies = axios.create({
                withCredentials: true
            })
            await axiosWithCookies.get('http://localhost:5000/logout')
                .then(res => {
                    this.isAuthenticated = false
                }).catch(err => {
                    console.log(err)
                })
        },
        async getCSRF() {
            let axiosWithCookies = axios.create({
                withCredentials: true
            })
            await axiosWithCookies.get('http://localhost:5000/getcsrf')
                .then(res => {
                    this.csrfToken = res.headers.get(["X-CSRFToken"]);
                }).catch(err => {
                    console.log(err)
                })
        },
        async getSession() {
            let axiosWithCookies = axios.create({
                withCredentials: true
            })
            await axiosWithCookies.get('http://localhost:5000/getsession')
                .then(res => {
                    if (res.data["status"] == "success") {
                        this.isAuthenticated = true
                        console.log(res)
                    } else {
                        this.isAuthenticated = false
                        this.getCSRF()
                        console.log(res)
                        console.log("")
                    }
                }).catch(err => {
                    console.log(err)
                })
        }
    }
})




 // async verAuth() {
        //     let authSent = {
        //         "frontKey": this.getCookie("session")
        //     }

        //     if (authSent["frontKey"] != "") {
        //         let axiosWithCookies = axios.create({
        //             withCredentials: true
        //         })
        //         await axiosWithCookies.post('http://localhost:5000/verAuth', authSent)
        //             .then(res => {
        //                 if (res.data["status"] == "success") {
        //                     console.log(res)
        //                     this.isLoggedIn = true
        //                 } else {
        //                     console.log(res)
        //                     this.isLoggedIn = false
        //                 }
        //             }).catch(err => {
        //                 console.log(err)
        //                 this.isLoggedIn = false
        //             })
        //     } else {
        //         this.isLoggedIn = false
        //     }
        // }