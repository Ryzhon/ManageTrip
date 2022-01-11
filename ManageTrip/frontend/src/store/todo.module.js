import { axios } from "@/common/api.service.js";


export default {
    state: {
        user_send:[],
        user_receive:[]

    },
    mutations:{
    },

    actions:{
        async triggerDeleteAnswer(context, answer) {    

            const endpoint = `/api/v1/todo/${answer.uuid}/`;
            try {
                await axios.delete(endpoint);
                console.log(context.rootState.trip.answers)
                 context.rootState.trip.answers.splice(context.rootState.trip.answers.indexOf(answer), 1);
                // this.userHasAnswered = false;
            } catch (error) {
                console.log(error.response);
                alert(error.response.statusText);
        }
          },
        calc_Send(context,{user:user, fig:fig}) {
            if (context.state.user_send[user]) {
              context.state.user_send[user] = context.state.user_send[user] + fig;
            } else {
              context.state.user_send[user] = fig;
            }
          },
        calc_Receive(context,{user:user, fig:fig}) {
          if (context.state.user_receive[user]) {
            context.state.user_receive[user] = context.state.user_receive[user] + fig;
          } else {
            context.state.user_receive[user] = fig;
          }
        },
    changeTotal(context, {userF:userF,userT:userT, fig:fig, check:check}) {
      if (!check) {
        context.state.user_send[userF] = context.state.user_send[userF] - fig;
        context.state.user_receive[userT]= context.state.user_receive[userT] - fig
      } else {
        context.state.user_send[userF] = context.state.user_send[userF] + fig;
        context.state.user_receive[userT] = context.state.user_receive[userT] + fig;
      }
    },

    },
    getters: {

    }
  }