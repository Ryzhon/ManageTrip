<template>
  <div class="h-100 w-full flex items-center justify-start bg-teal-lightest font-sans">
    <div class="bg-white rounded shadow-lg p-6 m-4 w-full lg:w-3/4 lg:max-w-lg text-center">
      <input
        type="checkbox"
        id="check"
        v-model="checked"
        @click="this.$store.dispatch('changeTotal',{userF:this.answer.From,userT:this.answer.To,fig:this.answer.charge,check:this.checked})"
      />
      <label for="check" v-show="!checked">
        <span class="mr-3">
          From:{{ answer.From }}
        </span>
        <span>
          To:{{ answer.To }}
        </span>
        <div class="text-center">
          <span class="mr-5 ml-5">
            Content:{{ answer.body }}
          </span>
          <span>
            Charge:{{ answer.charge }}
          </span>
        </div>
        <div class="mt-3 text-center">
          <button class="border-2 border-teal-500 rounded shrink mr-5">
            <router-link
              :to="{name: 'todo-editor',params: { uuid: answer.uuid, content: answer.body }}"
            >
            Edit   
            </router-link>
          </button>
          <button
            @click="showDeleteConfirmationBtn = !showDeleteConfirmationBtn"
            class="border-2"
          >
            Delete
          </button>
          <button v-show="showDeleteConfirmationBtn" @click="$store.dispatch('triggerDeleteAnswer', this.answer);
          this.$store.dispatch('changeTotal',{userF:this.answer.From,userT:this.answer.To,fig:this.answer.charge,check:this.checked});
          this"

            class="border-2 ml-2 text-right"> 
            Yes, delete
          </button>
            </div>
        </label>  
    </div>
  </div>
</template>

<script>
export default {
  name: "TodoComponent",
  props: {
    answer: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      checked: false,
      showDeleteConfirmationBtn: false,
    };
  },
  created() {
    this.$store.dispatch("calc_Send", {user:this.answer.From,fig:this.answer.charge});
    this.$store.dispatch("calc_Receive", {user:this.answer.To, fig:this.answer.charge});
    
  },
};
</script>