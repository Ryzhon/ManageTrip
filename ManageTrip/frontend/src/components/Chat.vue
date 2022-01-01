<template>
    <div>
  <h1>welcome to the room</h1>
  <div>

  </div>
  <div id="messagescontainer">
    <h3 v-for="chat in chats" :key="chat.id">
        <p>{{ chat }}</p>
    </h3>
        </div>
        <div>
            <input type="text" name="" id="messageinputfield">
            <input type="submit" name="" id="sendbutton" value="send" @click="sendMessage">
        </div>
                <button
          v-show="next"
          @click="getTripChats"
        >
          Load More
        </button>
</div>
</template>

<script>
import { axios } from "@/common/api.service.js"

export default {
    name:"ChatComponent",
    props:{
        slug:{
            type:String,
            required:true
        },
        loginUser:{
            type:String,
            required:true
        }
    },
    data(){
        return{
            next:null,
            connection:null,
            chats:[]
        }
    },
    methods:{
    async getTripChats() {
      // get a page of answers for a single question from the REST API's paginated 'Questions Endpoint'
      let endpoint = `/api/v1/trips/${this.slug}/chat/`
      if (this.next) {
        endpoint = this.next
      }
      try {
        const response = await axios.get(endpoint)
        this.chats.push(...response.data.results)
        // console.log(response.data.results)
        if (response.data.next) {
          this.next = response.data.next
        } else {
          this.next = null
        }
      } catch (error) {
        console.log(error.response)
        console.log("error")
        alert(error.response.statusText)
      }
    },
 //----------------------------------------------------------//       
    WebConnect(){
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket('ws://'+window.location.host+'/ws/chat/'+ this.slug +'/')
   },
    sendMessage(){
    const message = document.querySelector('#messageinputfield').value
    this.connection.send(JSON.stringify({'message': [this.loginUser]+':'+ message, "loginUser":this.loginUser}))
    document.querySelector('#messageinputfield').value = ''
    this.connection.onmessage = function(e){
    const data = JSON.parse(e.data)
    let store = data.message
    let b = store.split(':')
   
    if(b[0]===data.loginUser){
        document.querySelector('#messagescontainer').innerHTML += '<h3 style="text-align:right">'+data.message+'</h3>'
        console.log("you are succeeded")}else{
        document.querySelector('#messagescontainer').innerHTML += '<h3 style="text-align:left">'+data.message+'</h3>'}
    }
    },
    },
    created(){
    this.getTripChats(),
    this.WebConnect()
    },
    }
    
</script>