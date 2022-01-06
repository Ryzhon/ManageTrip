<template>
  <div id="nav">
    <NavbarComponent
    :send_charge="total_charge"
    :login_user="login_user"/>
  </div>
  <router-view/>
</template>
<script>
// import { axios } from "@/common/api.service.js";
import NavbarComponent from "@/components/Navbar.vue";


export default {
  name: "App",
  components:{
    NavbarComponent
  },
  
  created() {
    this.$store.dispatch('setUserInfo')
    this.$store.dispatch('getUserInfo')
  },
};
</script>