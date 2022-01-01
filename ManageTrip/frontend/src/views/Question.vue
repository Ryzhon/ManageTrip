<template>
<div>
<div>
  <h1>{{ Subject.content }}
  </h1>

</div>


  {{ this.loginUser }}
  will pay
  {{ this.user_send[this.loginUser] }}

  {{ this.loginUser }}
  will receive
  {{ this.user_receive[this.loginUser] }}
 <button @click="CreateBtn = !CreateBtn">Create Task</button>
      <div v-show="CreateBtn">
          <form @submit.prevent="onSubmit">
              <p>create task</p>
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

      </div>
         <TodoComponent
        v-for="answer in answers"
        :answer="answer"
        :key="answer.uuid"
        @delete-answer="deleteTask"
        @calc-send="calcSend"
        @calc-receive="calcReceive"
        @change-total="changeTotal"
      />
          <button
          v-show="next"
          @click="getTripsAnswers"
        >
          Load More
        </button>

<ChatComponent
:slug="this.slug"
:loginUser="this.loginUser"/>
</div>


</template>

<script>
import { axios } from "@/common/api.service.js";
import TodoComponent from "@/components/Todo.vue"
import ChatComponent from "@/components/Chat.vue"

export default{
    name: "Trip",
    components:{
        TodoComponent,
        ChatComponent
    },
    data(){
        return {
            question:{},
            answers: [],
            todoFrom:null,
            todoTo:null,
            todoCharge:null,
            todoContent:null,
            userOpt:[],
            pkFrom: null,
            pkTo: null,
            CreateBtn:false,
            user_send:{},
            user_receive:{},
            loginUser:null,
            next: null,
            Subject:null,
            connection:null,

        }
    },
    props: {
    slug: {
      type: String,
      required: true,
    },
    // send_charge:{
    // type: Object,
    // required: true
    // }
    },
    methods:{
        async getTripsData(){
            const endpoint=`/api/v1/trips/${this.slug}/`;
            try {
            const response = await axios.get(endpoint);
            this.Subject = response.data
            // console.log(this.Subject)
            } catch (error) {
                console.log(error)
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
        console.log("error")
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
      console.log(this.todoContent,this.todoCharge,this.todoFrom,this.todoTo)
      let pkFrom = await this.ToIdFrom(this.todoFrom)
   
      let pkTo = await this.ToIdTo(this.todoTo)

      console.log(this.todoContent,this.todoCharge,pkFrom,pkTo)
      try {
        const response = await axios.post(endpoint, {
          body: this.todoContent,
          charge:this.todoCharge,
          From: pkFrom,
          To: pkTo

        });
        

        this.todoFrom = null
        this.todoTo = null
        this.todoContent = null
        this.todoCharge = null
        pkFrom = null
        pkTo = null
        console.log(response)

        if (this.error) {
          this.error = null;
        }
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    async ToIdFrom(Name){
        const endpoint='/api/v1/userinfo/';
        try {
        let userId = null
        const response = await axios.get(endpoint)
        for (let i = 0; i < response.data.results.length; i++) {
            userId = response.data.results[i]
            this.userOpt.push(userId.username) 
        }
        return response.data.results[this.userOpt.indexOf(Name)].id
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
    async ToIdTo(Name){
        const endpoint='/api/v1/userinfo/';

        try {
        let userId = null
        const response = await axios.get(endpoint)
        for (let i = 0; i < response.data.results.length; i++) {
            userId = response.data.results[i]
            this.userOpt.push(userId.username)
  
            
        }
        // console.log(response.data.results[this.userOpt.indexOf("admin")].id)
        return response.data.results[this.userOpt.indexOf(Name)].id
        // console.log(this.todoTo)
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
    async deleteTask(answer){
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
    calcSend(user, fig){
    if(this.user_send[user]){
      this.user_send[user]=this.user_send[user]+fig
    }else{
      this.user_send[user] = fig 
    }

    },
    calcReceive(user, fig){
      if(this.user_receive[user]){
      this.user_receive[user]=this.user_receive[user]+fig
    }else{
      this.user_receive[user] = fig 
    }
    },
    changeTotal(userF, fig, check){
      if(!check){
        this.user_send[userF] = this.user_send[userF]-fig
      }else{
        this.user_send[userF] = this.user_send[userF]+fig

      }
      console.log("changetotal working")
    },

    getLogin(){
      this.loginUser=window.localStorage.getItem("username")
    },
//---------------------------------------------------------------------------//

  
    
    
    },



    created(){
            this.getTripsAnswers(),
            this.getUserInfo()
            this.getLogin()
            this.getTripsData()
            
   
        },
        
}

</script>

<style scoped>

</style>