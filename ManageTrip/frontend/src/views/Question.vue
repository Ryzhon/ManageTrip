<template>
  <div >
    <div class="text-center box-content border-4 mt-5 mx-10 mb-5">
      <div class="text-xl my-2" v-if="getSubjectContent">
      {{ Subject.content }}
      </div>
      <div class="my-2">
    {{ loginUser }}
    will pay
    {{ this.user_send[this.loginUser] }}

    {{ this.loginUser }}
    will receive
    {{ this.user_receive[this.loginUser] }}
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
        <input
          type="number"
          id="charge"
          placeholder="charge"
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
        class="border-2 border-teal-500 rounded mr-2">Submit to Create Task!</button>
      </form>
    </div>
    <TodoComponent
      id="todoTask"
      v-for="answer in answers"
      :answer="answer"
      :key="answer.uuid"
      @delete-answer="deleteTask"
      @calc-send="calcSend"
      @calc-receive="calcReceive"
      @change-total="changeTotal"
    />
    <button v-show="next" @click="getTripsAnswers">Load More</button>

    <ChatComponent :slug="this.slug" :loginUser="this.loginUser" />
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

    async getTripsAnswers() {
      // get a page of answers for a single question from the REST API's paginated 'Questions Endpoint'
      let endpoint = `/api/v1/trips/${this.slug}/todos/`;
      if (this.next) {
        endpoint = this.next;
      }
      try {
        const response = await axios.get(endpoint);
        this.answers.push(...response.data.results);
        // console.log(response.data.results)
        if (response.data.next) {
          this.next = response.data.next;
        } else {
          this.next = null;
        }
      } catch (error) {
        console.log(error.response);
        console.log("error");
        alert(error.response.statusText);
      }
    },

    async onSubmit() {
      // Tell the REST API to create a new answer for this question
      // based on the user input, then update some data properties
      if (!this.todoContent) {
        this.error = "You can't send an empty answer!";
        return;
      }
      const endpoint = `/api/v1/trips/${this.slug}/todo/`;
      console.log(
        this.todoContent,
        this.todoCharge,
        this.todoFrom,
        this.todoTo
      );
      let pkFrom = await this.ToIdFrom(this.todoFrom);
      let pkTo = await this.ToIdTo(this.todoTo);
      console.log(this.todoContent, this.todoCharge, pkFrom, pkTo);
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

        const res = await axios.get(`/api/v1/trips/${this.slug}/todos/`)
        this.answers = res.data.results
        console.log(this.answers)


        // this.getTripsAnswers()



        // document.querySelector("#todoTask").innerHTML +=
        //     '<h3 style="text-align:left">' + "CreateTsk" + "</h3>";
        console.log(response);

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
        // console.log(response.data.results[this.userOpt.indexOf("admin")].id)
        return response.data.results[this.userOpt.indexOf(Name)].id;
        // console.log(this.todoTo)
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
        // console.log(response.data.results[this.userOpt.indexOf("admin")].id)
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    async deleteTask(answer) {
      // delete a given answer from the answers array and make a delete request to the REST API
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
      console.log("changetotal working");
    },

    getLogin() {
      this.loginUser = window.localStorage.getItem("username");
    },
    //---------------------------------------------------------------------------//
  },

  created() {
    this.getTripsAnswers(), 
    this.getUserInfo();
    this.getLogin();
    this.getTripsData();
  },
  computed:{
    getSubjectContent(){

      return this.Subject?.content
    }
  }
};
</script>

<style scoped>
</style>