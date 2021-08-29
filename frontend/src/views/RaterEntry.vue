<template>
  <div class="container">
    <div class="content">
      <router-link :to="{ name: 'group' }">
        <div class="card">
          <h2>Quote a New Case</h2>
          <p>Click here to quote a new case!</p>
        </div>
      </router-link>
      <router-link to="#">
        <div class="card">
          <h2>Scratchpad</h2>
          <p>Get started rating and create a new case later!</p>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "RaterEntry",
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

.card {
  width: 90%;
  height: 150px;
  margin: 1rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.3s;
}

.card:hover {
  transform: scale(1.05);
  background-color: #eee;
}

a {
  text-decoration: none;
}

a:link,
a:visited,
a:hover,
a:active {
  color: inherit;
}
</style>
