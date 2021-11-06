<template>
  <div class="container">
    <div class="content">
      <router-link :to="{ name: 'plan' }">
        <v-card
          class="mx-auto my-6 rounded-lg elevation-3 v-card d-flex align-center"
          color="primary"
        >
          <div class="v-card-icon mx-4">
            <v-icon large color="white"> mdi-plus-circle </v-icon>
          </div>
          <v-card-text>
            <h2 class="text-h4 font-weight-light white--text">
              Quote a New Case
            </h2>
            <p class="text-overline softer--text mt-2">
              Click here to quote a new case!
            </p>
          </v-card-text>
        </v-card>
      </router-link>

      <router-link :to="{ name: 'plan' }">
        <v-card
          class="mx-auto my-6 rounded-lg elevation-3 v-card d-flex align-center"
        >
          <div class="v-card-icon mx-4">
            <v-icon large color="primary"> mdi-plus-circle </v-icon>
          </div>
          <v-card-text>
            <h2 class="text-h4 font-weight-thin">Scratchpad</h2>
            <p class="text-overline primary--text mt-2">Get started quickly!</p>
          </v-card-text>
        </v-card>
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

.text-overline {
  line-height: 0.9rem;
}

a {
  text-decoration: none;
}

.v-card {
  transition: all 0.3s;
}

.v-card:hover {
  transform: scale(1.03);
}
</style>
