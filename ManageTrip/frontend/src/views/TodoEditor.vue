<template>
  <div>
    <h1>Edit Your Task</h1>
    <p>{{ content }}</p>
    <form @submit.prevent="onSubmit">
              <label for="from" >From</label>         
              <select id="from" v-model="todoFrom">
                  <option v-for="user in userOpt" :key="user.id" >{{user}}</option>
              </select>
              <label for="to">To</label>
              <select id="to" v-model="todoTo">
                  <option v-for="user in userOpt" :key="user.id">{{user}}</option>
              </select>
              <label for="charge"></label>
              <input type="number" id="charge" placeholder="charge" v-model="todoCharge">
              <label for="content"></label>
              <input type="text" id="content" placeholder="diner" v-model="todoContent">
              <button type="submit">Submit to Create Task!</button>
          </form>
    <p v-if="error" class="muted mt-2">{{ error }}</p>
  </div>
</template>

<script>
import { axios } from "@/common/api.service.js";
export default {
  name: "TodoEditor",
  props: {
    uuid: {
      type: String,
      required: true,
    },
    content:{
        type:String,
        required: true
    }
  },
  data() {
    return {
      questionSlug: null,
      answerBody: null,
      error: null,
      userOpt:[],
      todoTo:null,
      todoFrom:null,
      todoCharge: null,
      todoContent:null
    };
  },
  methods: {
    async onSubmit() {
      if (!this.answerBody) {
        this.error = "You can't submit an empty answer!";
        return;
      }
      const endpoint = `/api/v1/todo/${this.uuid}/`;
      try {
        await axios.put(endpoint, { body: this.answerBody });
        this.$router.push({
          name: "question",
          params: { slug: this.questionSlug },
        });
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
            this.userOpt.push(userId.username)   
        }
        // console.log(response.data.results[this.userOpt.indexOf("admin")].id)
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
  },
  

//   async beforeRouteEnter(to, from, next) {
//     // get the answer's data from the REST API and set two data properties for the component
//     const endpoint = `/api/v1/answers/${to.params.uuid}/`;
//     try {
//       const response = await axios.get(endpoint);
//       return next(
//         (vm) => (
//           (vm.answerBody = response.data.body),
//           (vm.questionSlug = response.data.question_slug)
//         )
//       );
//     } catch (error) {
//       console.log(error);
//     }
//   },
created(){
    this.getUserInfo()
}
};
</script>