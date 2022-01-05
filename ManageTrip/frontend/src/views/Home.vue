<template>
  <div class="bg-slate-100 h-screen">
	  <div class="flex flex-col w-auto p-10 items-center justify-center">
		  <div>
        <div v-for="trip in trips" :key="trip.uuid">
          <p class="mt-7 bg-white p-6 rounded-lg text-gray-500 shadow-lg text-lg w-screen mx-2">
            <router-link
            :to="{ name: 'trip', params:{ slug: trip.slug }}"
            >
            {{ trip.content }}
            <span class="text-sm ml-3">作成者:{{ trip.author }}</span>
            </router-link></p>
        </div>
      </div>
	  </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { axios } from "@/common/api.service.js";

export default {
  name: 'Home',
   data(){
     return {
     trips:[],
     User:[],
     Money:[],
     loginUser:null
 
     }
  },
  methods:{
    async getQuestion(){
      const endpoint = "/api/v1/trips/";
        try {
        const response = await axios.get(endpoint);
        this.trips.push(...response.data.results);
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
    }
  },
  async getUserInfo(){
        const endpoint='/api/v1/userinfo/';
        try {
        let userId = null
        const response = await axios.get(endpoint)
  
        for (let i = 0; i < response.data.results.length; i++) {
            userId = response.data.results[i]
            this.Money.push(userId.total_charge)
            this.User.push(userId.username)
        }        
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    getLoginUser(){
      this.loginUser = window.localStorage.getItem("username")
    }

  },
 
  created(){
    this.getQuestion()
    this.getUserInfo()
    this.getLoginUser()
  }
}
</script>
