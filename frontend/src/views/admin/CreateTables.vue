<template>
  <div class="container">
    <div class="content" v-if="loaded">
      <h1>{{ data }}</h1>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "CreateTables",
  data() {
    return {
      loaded: false,
      data: null,
      show: true,
    };
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/admin/create-tables");
    this.data = { ...res.data };
    this.loaded = true;
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
