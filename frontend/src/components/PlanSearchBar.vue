<template>
  <v-autocomplete
    dense
    rounded
    solo-inverted
    clearable
    v-model="model"
    :items="items"
    :loading="isLoading"
    :search-input.sync="search"
    color="white"
    hide-no-data
    hide-selected
    item-text="plan_description"
    item-value="plan_id"
    label="Search for a plan"
    prepend-icon="mdi-magnify"
    return-object
    @input="$emit('search:selected', model)"
  ></v-autocomplete>
</template>

<script>
import axios from "../services/axios.js";
export default {
  name: "PlanSearchBar",
  data() {
    return {
      searchURL: "/search/plan",
      search: null,
      model: null,
      data: [],
      isLoading: false,
    };
  },
  computed: {
    items() {
      if (this.data) {
        return this.data.map((item) => {
          return {
            ...item,
            plan_description: `Plan: ${item.plan_id}`,
          };
        });
      }
      return [];
    },
  },
  watch: {
    search(val) {
      if (!val) {
        this.data = [];
        return;
      }

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      // Lazily load input items
      axios
        .get(this.searchURL, {
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

<style></style>
