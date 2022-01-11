<template>
  <div class="bg-slate-100 h-screen">
	  <div class="flex flex-col w-auto p-10 items-center justify-center">
		  <div>
        <div v-for="trip in $store.state.trip.trips" :key="trip.uuid">
          <p class="mt-7 bg-white p-6 rounded-lg text-gray-500 shadow-lg text-lg w-screen mx-2">
            <router-link
              :to="{ name: 'trip', params: { slug: trip.slug }}">
              {{ trip.content }}
            <span class="text-sm ml-3">作成者:{{ trip.author }}</span>
            </router-link></p>
            <travelActions :slug="trip.slug" />    
        </div>
      </div>
	  </div>
  </div>
</template>

<script>
import travelActions from "@/components/travelAction.vue";

export default {
  name: 'Home',
  components:{
    travelActions
  },
  created(){
    this.$store.dispatch("getQuestion")
  }

  
}
</script>
