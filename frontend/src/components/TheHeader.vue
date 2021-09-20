<template>
  <v-app-bar app color="primary" dark clipped-left>
    <div class="d-flex align-center">
      <v-img
        alt="Vuetify Logo"
        class="shrink mr-2"
        contain
        src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
        transition="scale-transition"
        width="40"
      />
      <v-toolbar-title
        ><span class="brand-name-front secondary--text">Pi</span
        ><span class="brand-name-back">Rate</span></v-toolbar-title
      >
    </div>

    <v-spacer></v-spacer>
  </v-app-bar>
</template>

<script>
export default {
  name: "TheHeader",
};
</script>

<style scoped>
.brand-name-front {
  font-weight: 500;
  font-size: 2rem;
  text-transform: lowercase;
  font-family: "Wallpoet", cursive;
}
.brand-name-back {
  font-weight: 200;
  font-size: 2rem;
  text-transform: lowercase;
  font-family: "Wallpoet", cursive;
}

.dummy-fonts {
  font-family: "Griffy", cursive;
  font-family: "Metal Mania", cursive;
  font-family: "Monofett", cursive;
  font-family: "Train One", cursive;
  font-family: "Turret Road", cursive;
  font-family: "Uncial Antiqua", cursive;
  font-family: "Wallpoet", cursive;
}
</style>
