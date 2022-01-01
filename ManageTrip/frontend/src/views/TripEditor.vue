<template>
  <div>
    <h1>Where did you go?</h1>
    <form @submit.prevent="onSubmit">
      <textarea
        v-model="TripBody"
        placeholder="Tourist site"
        rows="1"
      ></textarea>
      <button type="submit">Publish</button>
    </form>
    <p v-if="error">{{ error }}</p>
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