<template>
  <div v-if="loaded">
    <app-form-card
      :stages="stages"
      :title="title"
      :subtitle="subtitle"
      @toggle:stage="toggleHandler"
    >
      <template #content>
        <div class="grid grid-cols-4">
          <app-tile
            v-for="tile in tiles"
            :key="tile.id"
            :text="tile.text"
            class="bg-cover bg-center"
            background="bg-grad-violet-indigo"
            :selected="checkedHandler(tile.id)"
            @update:selection="selectionHandler(tile)"
            @dblclick="routeHandler"
          >
            <component :is="tile.icon" class="h-1/2 w-1/2 text-white" />
          </app-tile>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button class="mx-3" :disabled="!selection" @click="routeHandler"
            >Next</app-button
          >
        </div>
      </template>
    </app-form-card>
  </div>
</template>

<script>
export default {
  name: "Config_DistributionLanding",
  props: {},
  async mounted() {
    this.loaded = false;
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      title: "Add Some Distributions",
      subtitle: "",
      stages: [
        { label: "All Products", id: "products", to: "config-product-list" },
        {
          label: "Distributions",
          id: "distributions",
          active: true,
          to: "config-distribution-landing",
        },
      ],
      tiles: [
        {
          text: "Age",
          icon: "plus-circle-icon",
          id: "age_distributions",
          route_name: "config-age-distribution-list",
        },
        {
          text: "Gender",
          icon: "plus-circle-icon",
          id: "gender_distributions",
          route_name: "config-gender-distribution-list",
        },
        {
          text: "Smoker",
          icon: "plus-circle-icon",
          id: "smoker_distributions",
          route_name: "config-smoker-status-distribution-list",
        },
      ],
      selection: null,
    };
  },
  methods: {
    checkedHandler(key) {
      if (this.selection) {
        return this.selection.id === key;
      }
      return false;
    },
    selectionHandler(val) {
      this.selection = val;
    },
    routeHandler() {
      if (this.selection) {
        this.routeTo(this.selection.route_name);
      }
    },
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        query: { ...query },
      });
    },
    toggleHandler(s) {
      const stage = this.stages.find((stg) => stg.id === s.id);
      this.routeTo(stage.to);
    },
  },
};
</script>
