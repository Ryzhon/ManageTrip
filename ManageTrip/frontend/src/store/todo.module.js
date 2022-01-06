import { axios } from "@/common/api.service.js";


export default {
    state: {
        answers:[]
    },
    mutations:{
    },

    actions:{
        async triggerDeleteAnswer(context, answer) {
            // this.$emit("delete-answer", this.answer);
            const endpoint = `/api/v1/todo/${answer.uuid}/`;
            try {
                await axios.delete(endpoint);
                // context.state.answers.splice(context.state.answers.indexOf(answer), 1);
                // this.userHasAnswered = false;
            } catch (error) {
                console.log(error.response);
                alert(error.response.statusText);
      }
          },
          triggerSend() {
            this.$emit("calc-send", this.answer.From, this.answer.charge);
          },
          triggerReceive() {
            this.$emit("calc-receive", this.answer.To, this.answer.charge);
          },
          changeTotal() {
            this.$emit(
              "change-total",
              this.answer.From,
              this.answer.To,
              this.answer.charge,
              this.checked
            );
          },

    },
    getters: {

    }
  }