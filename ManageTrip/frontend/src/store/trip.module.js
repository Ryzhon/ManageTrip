import { axios } from "@/common/api.service.js";

export default {
    state: {
      answers:[],
      next: null,
      todoForm: null,
      todoTo: null
    },
    mutations:{

    },
    actions:{
      async getTripsAnswers(context, slug) {
        let endpoint = `/api/v1/trips/${slug}/todos/`;
        if (context.state.next) {
          endpoint = context.state.next;
        }
        console.log("working")
        try {
          const response = await axios.get(endpoint);
          context.state.answers.push(...response.data.results);
          if (response.data.next) {
            context.state.next = response.data.next;
          } else {
            context.state.next = null;
          }
          console.log(response)
        } catch (error) {
          console.log(error.response)
          alert(error.response.statusText);
        }
      },
      //------------------------------------------
      async onSubmit(context,slug, todoContent, charge) {
        if (!todoContent) {
          this.error = "文字を入力してください";
          return;
        }
        const endpoint = `/api/v1/trips/${slug}/todo/`;
        let pkFrom = await this.ToIdFrom(context.state.todoFrom);
        let pkTo = await this.ToIdTo(context.state.todoTo);
        try {
          const response = await axios.post(endpoint, {
            body: todoContent,
            charge: charge,
            From: pkFrom,
            To: pkTo,
          });
          context.state.todoFrom = null;
          context.state.todoTo = null;
          // todoContent = null;
          //コンポーネントからもらった値をnullにして返したい
          this.todoCharge = null;
          pkFrom = null;
          pkTo = null;
          console.log(response)
          const res = await axios.get(`/api/v1/trips/${slug}/todos/`)
          this.answers = res.data.results
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
          //commit
          return response.data.results[this.userOpt.indexOf(Name)].id;
        } catch (error) {
          console.log(error.response);
          alert(error.response.statusText);
        }
      }

    },
    getters: {

    }
  }