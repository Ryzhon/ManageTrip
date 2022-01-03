<template>
<!-- <div>
  <div>
  </div>
  <div v-for="trip in trips" :key="trip.uuid">
    <div>
      <h1 > {{ trip.author }} </h1>
      <router-link
      :to="{ name: 'trip', params:{ slug: trip.slug } }">
        {{ trip.content }}
      </router-link>
    </div>
  </div>
</div> -->
<div class="bg-slate-100 h-screen">
	<div class="flex flex-col w-auto p-10 items-center justify-center">
		<div>
			<!-- <form class="bg-white rounded-md py-10 px-12 shadow-lg">
				<h1 class="text-xl mt-2 text-center font-semibold text-gray-600">Whrite Todo List</h1>
				<div
        class="mt-6 flex space-x-10 m-10 justify-center item-center">
					<input type="number" placeholder="0" min="0" class="cursor-pointer bg-gray-100 w-10 text-center rounded-md pl-2 outline-none py-2 border-2" />
					<input placeholder="" class="bg-gray-100 rounded-md py-2 px-4 border-2 outline-none"/>
					<button class="bg-yellow-400 px-4 rounded-md font-semibold">Send</button>
				</div>
				
		</form> -->
    <!-- v-for="trip in trips" :key="trip.uuid" --> 
   <div v-for="trip in trips" :key="trip.uuid">
		<p class="mt-7 bg-white p-6 rounded-lg text-gray-500 shadow-lg text-lg w-screen mx-2"><router-link
     
      :to="{ name: 'trip', params:{ slug: trip.slug }}"
      >
        {{ trip.content }} <span class="text-sm ml-3">作成者:{{ trip.author }}</span>
      </router-link></p></div>
      <!-- <p class="mt-6 bg-white p-6 rounded-md text-gray-500 shadow-lg"> lkasjdlfkas </p> -->
      <!-- <p  class="item-center mt-6 bg-white p-6 rounded-md text-gray-500 shadow-lg"><a href="">first laskjdflksaf </a> </p>
      <p class="mt-6 bg-white p-6 rounded-md text-gray-500 shadow-lg"><a href=""> second laksjdfs</a></p> -->
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
      let endpoint = "/api/v1/trips/";
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
        console.log(this.User)
        console.log(this.Money)

        
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    getLoginUser(){
      this.loginUser = window.localStorage.getItem("username")
      console.log(this.loginUser)
    }

  },
 
  created(){
    this.getQuestion()
    this.getUserInfo()
    this.getLoginUser()
  }
}
</script>
