import { axios } from "@/common/api.service.js";


export default {
    state: {
        set_login_user:null,
        get_login_user:null,
        userOpt: []
    },
    mutations:{
        UPDATE_USERCHARGE(state, user){
            state.userOpt = user
        }
    },
    actions:{
        async setUserInfo(context) {
            try {
              const response = await axios.get("/auth/users/me/");
              const requestUser = response.data["username"]
              window.localStorage.setItem("username", requestUser);
              context.state.set_login_user=window.localStorage.getItem("username")
              
            } catch (error) {
              console.log(error.response);
              alert(error.response.statusText);
            }
        },
        async getUserInfo(context){
            const endpoint='/api/v1/userinfo/';
            try {
            let userId = null
            const user = []
            const response = await axios.get(endpoint)
            for (let i = 0; i < response.data.results.length; i++) {
               userId = response.data.results[i]
               user.push(userId.username)
            //    userCharge = Object.assign({}, context.state.total_charge, {[context.state.userOpt[i]]:0})
            }
            context.commit("UPDATE_USERCHARGE", user)
          } catch (error) {
            console.log(error.response);
            alert(error.response.statusText);    
          }
        },
        getLogin(context) {
            context.state.get_login_user = window.localStorage.getItem("username");
            },
        
    }
}