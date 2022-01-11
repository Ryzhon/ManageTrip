<template>
  <div>
    <h1>Edit Your Task</h1>
    <p>{{ content }}</p>
    <form @submit.prevent="onSubmit">
      <label for="from" >From</label>         
      <select id="from" v-model="todoFrom">
        <option v-for="user in this.$store.state.user.userOpt" :key="user.id" >{{user}}</option>
      </select>
      <label for="to">To</label>
      <select id="to" v-model="todoTo">
        <option v-for="user in this.$store.state.user.userOpt" :key="user.id">{{user}}</option>
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
        this.error = "文字を入力してください";
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
  },
created(){
    this.getUserInfo()
}
};
</script>