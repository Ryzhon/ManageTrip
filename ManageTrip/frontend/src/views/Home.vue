<template>


<div>
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
</div>
</template>

<script>
// @ is an alias to /src
import { axios } from "@/common/api.service.js";

export default {
  name: 'Home',
   data(){
     return {
     trips:[]
 
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

  },
 
  created(){
    this.getQuestion()
  }
}
</script>
