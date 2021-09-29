<template>
  <p>{{ session_data }}</p>
</template>

<script>
const axios = require("axios");

export default {
  name: "Session",
  data() {
    return {
      session_data: null,
    };
  },
  async mounted() {
    this.plan_id = this.$route.query.plan_id;
    const res = await axios.get(
      `http://localhost:5000/session/${this.plan_id}`,
      {
        withCredentials: true,
      }
    );
    this.session_data = res.data;
  },
};
</script>

<style></style>
