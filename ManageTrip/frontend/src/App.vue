<template>
  <div id="nav">
    <NavbarComponent
    :login_user="$store.state.user.get_login_user"/>
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