<template>
  <div class="container">
    <div class="content my-6">
      <p>{{ session_data }}</p>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";

export default {
  name: "Session",
  data() {
    return {
      session_data: null,
    };
  },
  async mounted() {
    const res = await axios.get(`/admin/session-data`);
    this.session_data = res.data;
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
