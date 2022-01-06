<template>
  <div >
    <div class="text-center box-content border-4 mt-5 mx-10 mb-5">
      <div class="text-xl my-2" v-if="getSubjectContent">
        {{ Subject.content }}
      </div>
      <div class="my-2">
        {{ loginUser }}
        will pay
        {{ user_send[this.loginUser] }}
        {{ loginUser }}
        will receive
        {{ user_receive[this.loginUser] }}
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
            <option v-for="user in userOpt" :key="user.id">{{ user }}</option>
          </select>
        <label for="to" class="mr-2">To</label>
          <select id="to" v-model="todoTo"
            class="border-2 border-teal-500 rounded mr-2">
            <option v-for="user in userOpt" :key="user.id">{{ user }}</option>
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
      @delete-answer="deleteTask"
      @calc-send="calcSend"
      @calc-receive="calcReceive"
      @change-total="changeTotal"
    />
    <button v-show="next" @click="getTripsAnswers">Load More</button>

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
      question: {},
      answers: [],
      todoFrom: null,
      todoTo: null,
      todoCharge: null,
      todoContent: null,
      userOpt: [],
      pkFrom: null,
      pkTo: null,
      CreateBtn: false,
      user_send: {},
      user_receive: {},
      loginUser: null,
      next: null,
      Subject: null,
      connection: null,
    };
  },
  props: {
    slug: {
      type: String,
      required: true,
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
        const res = await axios.get(`/api/v1/trips/${this.slug}/todos/`)
        this.answers = res.data.results
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
          this.userOpt.push(userId.username);
        }
        return response.data.results[this.userOpt.indexOf(Name)].id;
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
          this.userOpt.push(userId.username);
        }
        return response.data.results[this.userOpt.indexOf(Name)].id;
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    async getUserInfo() {
      const endpoint = "/api/v1/userinfo/";
      try {
        let userId = null;
        const response = await axios.get(endpoint);
        for (let i = 0; i < response.data.results.length; i++) {
          userId = response.data.results[i];
          this.userOpt.push(userId.username);
        }
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    async deleteTask(answer) {
      const endpoint = `/api/v1/todo/${answer.uuid}/`;
      try {
        await axios.delete(endpoint);
        this.answers.splice(this.answers.indexOf(answer), 1);
        this.userHasAnswered = false;
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    calcSend(user, fig) {
      if (this.user_send[user]) {
        this.user_send[user] = this.user_send[user] + fig;
      } else {
        this.user_send[user] = fig;
      }
    },
    calcReceive(user, fig) {
      if (this.user_receive[user]) {
        this.user_receive[user] = this.user_receive[user] + fig;
      } else {
        this.user_receive[user] = fig;
      }
    },
    changeTotal(userF,userT, fig, check) {
      if (!check) {
        this.user_send[userF] = this.user_send[userF] - fig;
        this.user_receive[userT]= this.user_receive[userT] - fig
      } else {
        this.user_send[userF] = this.user_send[userF] + fig;
      }
    },

  },
  created() {
    this.$store.dispatch("getTripsAnswers", this.slug), 
    this.getUserInfo();
    this.$store.dispatch("getLogin")
    this.getTripsData();
  },
  computed:{
    getSubjectContent(){
      return this.Subject?.content
    },

  }
};
</script>
