<template>
  <div >
    <div class="text-center box-content border-4 mt-5 mx-10 mb-5">
      <div class="text-xl my-2" v-if="getSubjectContent">
        {{ Subject.content }}
      </div>
      <div class="my-2">
        {{ $store.state.user.get_login_user }}
        will pay
        <span >{{ $store.state.todo.user_send[$store.state.user.get_login_user] }}</span>
        {{ $store.state.user.get_login_user }}
        will receive
        <span>{{ $store.state.todo.user_receive[$store.state.user.get_login_user] }}</span>
      </div>
    </div>
    <div>
      <button
        @click="CreateBtn = !CreateBtn"
        class="border-2 border-teal-500 rounded ml-10">
        Create Task
      </button>
    </div>
    <div v-show="CreateBtn">
      <form @submit.prevent="onSubmit" class="form-control">
        <label for="from" class="mr-2">From</label>
          <select id="from" v-model="todoFrom"
            class="border-2 border-teal-500 rounded mr-2" >
            <option v-for="user in this.$store.state.user.userOpt" :key="user.id">{{ user }}</option>
          </select>
        <label for="to" class="mr-2">To</label>
          <select id="to" v-model="todoTo"
            class="border-2 border-teal-500 rounded mr-2">
            <option v-for="user in this.$store.state.user.userOpt" :key="user.id">{{ user }}</option>
          </select>
        <label for="charge"></label>
        <input type="number" id="charge" placeholder="charge"
          v-model="todoCharge"
          min='0'
          class="border-2 border-teal-500 rounded mr-2"
        />
        <label for="content"></label>
        <input
          type="text"
          id="content"
          placeholder="diner"
          v-model="todoContent"
          class="border-2 border-teal-500 rounded mr-2"
        />
        <button type="submit"
          class="border-2 border-teal-500 rounded mr-2">Submit to Create Task!
        </button>
      </form>
    </div>
    <TodoComponent
      id="todoTask"
      v-for="answer in this.$store.state.trip.answers"
      :answer="answer"
      :key="answer.uuid"
    />
    <button v-show="this.$store.state.trip.next" @click="this.$store.dispatch('getTripsAnswers')">Load More</button>
    <ChatComponent :slug="this.slug" :loginUser="this.$store.state.user.get_login_user" />
  </div>
</template>

<script>
import { axios } from "@/common/api.service.js";
import TodoComponent from "@/components/Todo.vue";
import ChatComponent from "@/components/Chat.vue";

export default {
  name: "Trip",
  components: {
    TodoComponent,
    ChatComponent,
  },
  data() {
    return {
      answers: [],
      todoFrom: null,
      todoTo: null,
      todoCharge: null,
      todoContent: null,
      pkFrom: null,
      pkTo: null,
      CreateBtn: false,
      next: null,
      Subject: null,
    };
  },
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  computed:{
    getSubjectContent(){
    return this.Subject?.content
    },
  },
  methods: {
    async getTripsData() {
      const endpoint = `/api/v1/trips/${this.slug}/`;
      try {
        const response = await axios.get(endpoint);
        this.Subject = response.data;
        console.log(this.Subject);
      } catch (error) {
        console.log(error);
      }
    },

    // async getTripsAnswers() {
    //   let endpoint = `/api/v1/trips/${this.slug}/todos/`;
    //   if (this.next) {
    //     endpoint = this.next;
    //   }
    //   try {
    //     const response = await axios.get(endpoint);
    //     this.answers.push(...response.data.results);
    //     if (response.data.next) {
    //       this.next = response.data.next;
    //     } else {
    //       this.next = null;
    //     }
    //     console.log(response)
    //   } catch (error) {
    //     console.log(error.response)
    //     alert(error.response.statusText);
    //   }
    // },

    async onSubmit() {
      if (!this.todoContent) {
        this.error = "文字を入力してください";
        return;
      }
      const endpoint = `/api/v1/trips/${this.slug}/todo/`;
      let pkFrom = await this.ToIdFrom(this.todoFrom);
      let pkTo = await this.ToIdTo(this.todoTo);
      try {
        const response = await axios.post(endpoint, {
          body: this.todoContent,
          charge: this.todoCharge,
          From: pkFrom,
          To: pkTo,
        });
        this.todoFrom = null;
        this.todoTo = null;
        this.todoContent = null;
        this.todoCharge = null;
        pkFrom = null;
        pkTo = null;
        console.log(response)
        this.$store.dispatch("getTripsAnswers", this.slug)
        if (this.error) {
          this.error = null;
        }
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    async ToIdFrom(Name) {
      const endpoint = "/api/v1/userinfo/";
      try {
        let userId = null;
        const response = await axios.get(endpoint);
        for (let i = 0; i < response.data.results.length; i++) {
          userId = response.data.results[i];
          this.$store.state.user.userOpt.push(userId.username);
        }
        return response.data.results[this.$store.state.user.userOpt.indexOf(Name)].id;
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    async ToIdTo(Name) {
      const endpoint = "/api/v1/userinfo/";
      try {
        let userId = null;
        const response = await axios.get(endpoint);
        for (let i = 0; i < response.data.results.length; i++) {
          userId = response.data.results[i];
          this.$store.state.user.userOpt.push(userId.username);
        }
        return response.data.results[this.$store.state.user.userOpt.indexOf(Name)].id;
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },

  },
  created() {
    this.$store.dispatch("getTripsAnswers", this.slug), 
    this.$store.dispatch("getLogin")
    this.getTripsData();
  },

};
</script>
