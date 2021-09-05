<template>
  <div id="app">
    <div class="container">
      <base-sidebar class="nav-container" />
      <div class="page-container">
        <div id="nav">
          <router-link to="/">Home</router-link> |
          <router-link to="/admin/create-tables">Create Tables</router-link> |
          <router-link :to="{ name: 'rater' }">Rater</router-link>
        </div>
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import BaseSidebar from "./components/BaseSidebar.vue";

export default {
  name: "App",
  components: {
    BaseSidebar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.container {
  display: flex;
  flex-direction: row;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.page-container {
  width: 85%;
}
</style>
