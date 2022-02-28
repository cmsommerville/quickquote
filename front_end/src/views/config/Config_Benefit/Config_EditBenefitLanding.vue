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
            :disabled="tile.disabled"
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
import axios from "@/services/axios.js";

export default {
  name: "Config_EditBenefitLanding",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    benefit_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    const bnft = await axios.get(`/config/benefit/${this.benefit_id}`);
    this.benefit = { ...bnft.data };

    this.tiles = [
      ...[
        {
          text: "Basic Info",
          icon: "plus-circle-icon",
          id: "benefit",
          route_name: "config-benefit-edit",
        },
        {
          text: "States",
          icon: "plus-circle-icon",
          id: "states",
          route_name: "config-benefit-states",
        },
        {
          text: "Durations",
          icon: "plus-circle-icon",
          id: "durations",
          disabled: !this.benefit.is_durational,
          route_name: "config-benefit-duration-list",
        },
      ],
    ];
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      stages: [
        {
          label: "Back to Benefits",
          id: "benefits",
          to: "config-benefits",
        },
        {
          label: "Configure",
          id: "configure",
          active: true,
          disabled: true,
        },
      ],
      tiles: [],
      selection: null,
      benefit: {},
    };
  },
  computed: {
    title() {
      return `Configure ${this.benefit.benefit_label}`;
    },
    subtitle() {
      return "Let's edit this benefit!";
    },
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
        const disabled = false;
        if (!disabled) {
          this.routeTo(this.selection.route_name);
        }
      }
    },
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id, benefit_id: this.benefit_id },
        query: { ...query },
      });
    },
    toggleHandler(stg) {
      const stage = this.stages.find((s) => s.id === stg.id);
      this.routeTo(stage.to);
    },
  },
};
</script>
