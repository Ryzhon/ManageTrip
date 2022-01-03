<template>
<!-- <div>
    <h1>Where did you go?</h1>
    <form @submit.prevent="onSubmit">
  
      <input
        v-model="TripBody"
        placeholder="Tourist site"
        v-on:keyup.enter="onSubmit"
      >
      <input type="submit" value="Publish">
    </form>
    <p v-if="error">{{ error }}</p>
  </div> -->

  <div class="min-h-screen bg-gray-100 flex justify-center items-center ">
  <div class="bg-white p-4 w-96 rounded-md shadow-lg" >
    <h1 class="text-lg font-bold text-gray-500">Where did you go?</h1>
    <!-- <div class="mt-5 mb-2 border-2 py-1 px-3 flex justify-between rounde-md"> -->
      <form @submit.prevent="onSubmit" class="mt-5 mb-2 border-2 py-1 px-3 flex justify-between rounde-lg">
      <input 
      
      class="flex-grow outline-none text-gray-600 focus:text-blue-600 " 
      type="text" 
      placeholder="Tourist site..."
      v-model="TripBody"
      v-on:keyup.enter="onSubmit" />
      <button  type="submit" class="w-content bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">Publish</button>
      </form>
    <!-- </div> -->
  </div>
</div>
  
</template>

<script>
import { axios } from "@/common/api.service.js";
export default {
  name: "TripEditor",
  props: {
    slug: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      TripBody: null,
      error: null,
    };
  },
  methods: {
    async performNetworkRequest() {
      // Tell the REST API to create or update a Question instance;
      let endpoint = "/api/v1/trips/";
      let method = "POST";
      if (this.slug !== undefined && this.slug !== "") {
        endpoint += `${this.slug}/`;
        method = "PUT";
      }
      try {
        const response = await axios({
          method: method,
          url: endpoint,
          data: { content: this.TripBody },
        });
        this.$router.push({
          name: "trip",
          params: { slug: response.data.slug },
        });
      } catch (error) {
        this.error = error.response.statusText;
      }
    },
    onSubmit() {
      // perform basic validation and eventually call this.performNetworkRequest;
      if (!this.TripBody) {
        this.error = "You can't send an empty question!";
      } else if (this.TripBody.length > 240) {
        this.error = "Ensure this field has no more than 240 characters!";
      } else {
        this.performNetworkRequest();
      }
    },
  },
//   async beforeRouteEnter(to, from, next) {
//     // if the component is used to update a question
//     // get the question's data from the REST API
//     if (to.params.slug !== undefined && to.params.slug !== "") {
//       const endpoint = `/api/v1/questions/${to.params.slug}/`;
//       try {
//         const response = await axios.get(endpoint);
//         return next((vm) => (vm.questionBody = response.data.content));
//       } catch (error) {
//         console.log(error.response);
//         alert(error.response.statusText);
//       }
//     } else {
//       return next();
//     }
//   },
  created() {
    document.title = "Editor - QuestionTime";
  },
};
</script>