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
    provision_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;
    const bnft = await axios.get(`/config/provision/${this.provision_id}`);
    this.provision = { ...bnft.data };

    this.tiles = [
      ...[
        {
          text: "Basic Info",
          icon: "plus-circle-icon",
          id: "provision",
          route_name: "config-provision-edit",
        },
        {
          text: "States",
          icon: "plus-circle-icon",
          id: "states",
          route_name: "config-provision-states",
        },
        {
          text: "UI",
          icon: "plus-circle-icon",
          id: "ui",
          route_name: "config-provision-ui",
        },
        {
          text: "Factors",
          icon: "plus-circle-icon",
          id: "factors",
          route_name: "config-factor-list",
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
          label: "Back to Provisions",
          id: "provisions",
          to: "config-provision-list",
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
      provision: {},
    };
  },
  computed: {
    title() {
      return `Configure ${this.provision.provision_label}`;
    },
    subtitle() {
      return "Let's edit this provision!";
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
        params: {
          product_id: this.product_id,
          provision_id: this.provision_id,
        },
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
