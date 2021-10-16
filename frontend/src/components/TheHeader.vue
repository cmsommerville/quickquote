<template>
  <div>
    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon
        @click.stop="$emit('click-hamburger')"
      ></v-app-bar-nav-icon>

      <v-toolbar-title>
        <span class="brand-name-front secondary--text">Pi</span
        ><span class="brand-name-back">Rate</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <v-autocomplete
        dense
        rounded
        solo-inverted
        clearable
        class="mt-6"
        v-model="model"
        :items="items"
        :loading="isLoading"
        :search-input.sync="search"
        color="white"
        hide-no-data
        hide-selected
        item-text="plan"
        item-value="plan_id"
        label="Public APIs"
        placeholder="Start typing to Search"
        prepend-icon="mdi-magnify"
        return-object
        @input="searchHandler"
      ></v-autocomplete>

      <v-spacer></v-spacer>
      <div>
        <v-btn plain :to="{ name: 'rater' }"> New Quote </v-btn>
      </div>
    </v-app-bar>
  </div>
</template>

<script>
import axios from "../services/axios.js";

export default {
  name: "TheHeader",
  data() {
    return {
      search: null,
      model: null,
      data: [],
      isLoading: false,
    };
  },

  computed: {
    items() {
      return this.data.map((item) => {
        return { ...item, plan: `PLAN-${item.plan_id}` };
      });
    },
  },
  methods: {
    searchHandler() {
      // handle input event for search br
      console.log("Search Click Handler");
    },
  },
  watch: {
    search(val) {
      // Items have already been loaded
      if (this.items.length > 0) return;

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      // Lazily load input items
      axios
        .get("/search/plan", {
          params: {
            plan_id: val,
          },
        })
        .then((res) => (this.data = res.data))
        .catch((err) => {
          console.log(err);
        })
        .finally(() => (this.isLoading = false));
    },
  },
};
</script>

<style scoped>
.header {
  width: 100%;
}
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
