<template>
  <div class="container">
    <div class="content">
      <button @click="createTables">Create Tables</button>
      <div class="response" v-if="created">
        <h2>{{ data.message }}</h2>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "CreateTables",
  data() {
    return {
      data: null,
      created: false,
    };
  },
  methods: {
    async createTables() {
      this.created = false;
      const res = await axios.get("http://localhost:5000/admin/create-tables");
      this.data = { ...res.data };
      this.created = true;
    },
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

.response {
  margin: 3rem 0;
}

button {
  padding: 1rem 2rem;
  background-color: rgb(101, 132, 255);
  border-radius: 10px;
  color: #fff;
  font-size: 1.5rem;
}
</style>
