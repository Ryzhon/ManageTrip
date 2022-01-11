<template>
  <div class="mt-3">
    <!-- <router-link
      :to="{ name: 'question-editor', params: { slug: slug } }"
      class="btn btn-sm"
      >Edit
    </router-link> -->
    <button
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-5"
      @click="showDeleteConfirmationBtn = !showDeleteConfirmationBtn"
    >
      Delete
    </button>
    <button
      v-show="showDeleteConfirmationBtn"
      class="bg-red-400 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-5"
      @click="deleteTravel"
    >
      本当に削除しますか？
    </button>
    <hr />
  </div>
</template>

<script>
import { axios } from "@/common/api.service.js";
export default {
  name: "travelActions",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showDeleteConfirmationBtn: false,
    };
  },
  methods: {
    async deleteTravel() {
      const endpoint = `/api/v1/trips/${this.slug}/`;
      try {
        await axios.delete(endpoint);
        this.$router.push({
          name: "home",
        });
        this.$store.state.trip.trips.shift()
      } catch (error) {
        console.log(error.response);
        alert(error.response.statusText);
      }
    },
  },
};
</script>
