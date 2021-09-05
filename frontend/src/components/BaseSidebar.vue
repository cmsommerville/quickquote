<template>
  <nav class="sidenav">
    <router-link :to="{ name: 'Home' }" class="logo">
      <div class="sidenav__logo">
        <span class="sidenav__logo-1">Q</span>
        <span class="sidenav__logo-2">Q</span>
      </div>
    </router-link>
    <ul class="sidenav__link-list">
      <li v-for="link in links" :key="link.to" class="sidenav__link-item">
        <router-link :to="{ name: link.to }">{{ link.label }}</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "BaseSidebar",
  data() {
    return {
      links: [
        { label: "Home", to: "Home" },
        { label: "New Quote", to: "rater" },
        { label: "Create Tables", to: "create-tables" },
      ],
    };
  },
};
</script>

<style scoped>
.sidenav {
  height: 100vh;
  width: 15%;
  background-color: #eee;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: auto;
}

.sidenav__logo {
  font-size: 5rem;
  font-weight: 700;
  position: relative;
  width: 100%;
  height: 150px;
  -webkit-text-stroke: 1px hsl(171, 31%, 30%);
}

.sidenav__logo-1 {
  position: absolute;
  color: hsl(171, 31%, 90%);
  top: 10px;
  left: 45px;
}
.sidenav__logo-2 {
  position: absolute;
  color: hsl(171, 31%, 66%);
  top: 30px;
  left: 75px;
}

.sidenav__link-list {
  padding-left: 0;
  width: 100%;
}

.sidenav__link-item {
  list-style: none;
  border-radius: 5px;
}

.sidenav__link-item:hover {
  background-color: #ddd;
}

.router-link-exact-active:not(.logo) {
  background-color: #ccc;
  border-radius: 5px;
}

a {
  text-decoration: none;
  padding: 0.5rem 0;
  display: inline-block;
  width: 100%;
}

a:link,
a:visited {
  color: inherit;
}
a:active {
  color: #ddd;
}
</style>
