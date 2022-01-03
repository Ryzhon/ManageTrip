<template>
  <div class="h-100 flex justify-end bg-teal-lightest font-sans">
    <div class="box-content h-auto p-4 border-4 bg-slate-50 mr-32">
      <div
        id="messagescontainer"
      >
        <h1 class="text-xl px-12">welcome to the room</h1>
        <div v-for="chat in chats" :key="chat.id">
          <h5
            v-if="chat.author === this.loginUser"
            class="text-lg"
            style="text-align: right">
            {{ chat.message }}<div class="text-xs ml-2">{{ chat.created_at }}</div>
          </h5>
          <h5 v-else style="text-align: left">
            {{ chat.message }}
            
          <span class="text-orange-700">{{ chat.created_at }}</span>
          </h5>
        </div>
      </div>

      <div class="mt-2">
        <input
          type="text"
          name=""
          id="messageinputfield"
          v-on:keyup.enter="sendMessage"
          class="border-2 border-teal-500 rounded mr-2"
        />
        <input
          type="submit"
          name=""
          id="sendbutton"
          value="send"
          @click="sendMessage"
          class="border-2 border-teal-500 rounded mr-2"
        />
      </div>
    </div>

    <button v-show="next" @click="getTripChats">Load More</button>
  </div>
</template>

<script>
import { axios } from "@/common/api.service.js";

export default {
  name: "ChatComponent",
  props: {
    slug: {
      type: String,
      required: true,
    },
    loginUser: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      next: null,
      connection: null,
      chats: [],
    };
  },
  methods: {
    async getTripChats() {
      // get a page of answers for a single question from the REST API's paginated 'Questions Endpoint'
      let endpoint = `/api/v1/trips/${this.slug}/chat/`;
      if (this.next) {
        endpoint = this.next;
      }
      try {
        const response = await axios.get(endpoint);
        await this.chats.push(...response.data.results);
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
    //----------------------------------------------------------//
    WebConnect() {
      console.log("Starting connection to WebSocket Server");
      this.connection = new WebSocket(
        "ws://" + window.location.host + "/ws/chat/" + this.slug + "/"
      );
    },
    sendMessage() {
      const message = document.querySelector("#messageinputfield").value;
      this.connection.send(
        JSON.stringify({
          message: [this.loginUser] + ":" + message,
          loginUser: this.loginUser,
        })
      );
      document.querySelector("#messageinputfield").value = "";
      this.connection.onmessage = function (e) {
        const data = JSON.parse(e.data);
        let store = data.message;
        let b = store.split(":");

        if (b[0] === data.loginUser) {
          console.log(data);
          document.querySelector("#messagescontainer").innerHTML +=
            '<h3 style="text-align:right">' + data.message + "</h3>";
          console.log("you are succeeded");
        } else {
          document.querySelector("#messagescontainer").innerHTML +=
            '<h3 style="text-align:left">' + data.message + "</h3>";
        }
      };
    },
  },
  created() {
    this.getTripChats(), this.WebConnect();
  },
};
</script>