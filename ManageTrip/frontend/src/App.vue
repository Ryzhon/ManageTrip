<template>
  <div id="nav">
    <NavbarComponent
    :send_charge="total_charge"
    :login_user="login_user"/>
  </div>
  <router-view
  />
</template>
<script>
import { axios } from "@/common/api.service.js";
import NavbarComponent from "@/components/Navbar.vue";


export default {
  name: "App",
  components:{
    NavbarComponent
  },
  data(){
    return{
    userOpt:[],
     total_charge:[],
     login_user:null,
    

    }
  },


  methods: {
    async setUserInfo() {
      // add the username of the current user to localStorage
      try {
        const response = await axios.get("/auth/users/me/");
        const requestUser = response.data["username"];
        console.log("try works")
        window.localStorage.setItem("username", requestUser);
        this.login_user=window.localStorage.getItem("username")
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
           this.total_charge = Object.assign({}, this.total_charge, {[this.userOpt[i]]:0})
        }
        // this.$set(this.someObj, this.userOpt[0], 0)
        // console.log(this.userOpt[0])
        // console.log(this.total_charge["admin"])
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
        
      } 
  }
  },
  created() {
    this.setUserInfo();
    this.getUserInfo()
    
  },
};
</script>