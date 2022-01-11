import { axios } from "@/common/api.service.js";

export default {
    state: {
      answers:[],
      trips: [],
      next: null,
      todoForm: null,
      todoTo: null
    },
    mutations:{

      UPDATE_NEXT(state, next){
        state.next = next
      }
    },
    actions:{
      async getTripsAnswers(context, slug) {
        let endpoint = `/api/v1/trips/${slug}/todos/`;
        if (context.state.next) {
          endpoint = context.state.next;
        }
        try {
          const response = await axios.get(endpoint);
          
          context.state.answers.unshift(...response.data.results);
          // context.commit("UPDATE_ANSWERS", answer_list)
          if (response.data.next) {
            const next = response.data.next;
            context.commit("UPDATE_NEXT",next)
          } else {
            const next = null;
            context.commit("UPDATE_NEXT",next)
          }
          
        } catch (error) {
          console.log(error.response)
          alert(error.response.statusText);
        }
      },
      async getQuestion(context){
        const endpoint = "/api/v1/trips/";
          try {
          const response = await axios.get(endpoint)
          context.state.trips.push(...response.data.results)
        } catch (error) {
          console.log(error.response)
          alert(error.response.statusText)
        }
      },
    },
    getters: {

    }
  }