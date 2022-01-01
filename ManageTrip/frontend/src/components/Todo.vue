<template>
    <div>
        <input type="checkbox" id="check"       
        v-model="checked"
        @click="changeTotal">
        <label for="check"
        v-show="!checked"
         >
        From
            {{ answer.From }}
        To
            {{ answer.To }}
        Content
            {{ answer.body }}
        Charge
            {{ answer.charge }}
        <router-link
        :to="{ name: 'todo-editor', params: { uuid: answer.uuid, content: answer.body }}"
        >Edit
      </router-link>
      <button
        @click="showDeleteConfirmationBtn = !showDeleteConfirmationBtn"
      >
        Delete
      </button>
        </label>

      <button
        v-show="showDeleteConfirmationBtn"
      
        @click="triggerDeleteAnswer"
      >
        Yes, delete my answer!
      </button>
          <hr>
    </div>

</template>

<script>
export default {
    name: "TodoComponent",
    props: {
        answer: {
        type: Object,
        required: true,
    }
    },
    data(){
        return {
            checked:false,
            showDeleteConfirmationBtn:false,
            
        }
    },
    methods:{
        triggerDeleteAnswer(){
            this.$emit("delete-answer", this.answer)
        },
        triggerSend(){
            this.$emit("calc-send",this.answer.From ,this.answer.charge)
        },
        triggerReceive(){
            this.$emit("calc-receive", this.answer.To, this.answer.charge)
        },
        changeTotal(){
            this.$emit("change-total", this.answer.From, this.answer.charge, this.checked)
    
        }
        

    },
    created(){
        this.triggerSend();
        this.triggerReceive()
    }
    

}
</script>