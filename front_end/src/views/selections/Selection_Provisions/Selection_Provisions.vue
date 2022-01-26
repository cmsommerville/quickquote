<template>
  <div v-if="loaded">
    <app-form-card :stages="stages" :title="title" :subtitle="subtitle">
      <template #content>
        <div class="grid grid-cols-2 gap-8">
          <component
            v-for="prov in provisions"
            :key="prov.provision_id"
            :is="prov.ui_component.component_type_code"
            item_text="item_label"
            item_value="item_code"
            v-bind="prov.ui_component"
            v-model="prov.ui_provision_value"
            >{{ prov.ui_component.label }}</component
          >
        </div>
      </template>

      <template #actions>
        <div class="flex justify-center">
          <app-button
            class="mx-3 border-theme-primary bg-theme-primary text-white"
            @click="save"
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
  name: "SelectionBenefits",
  props: {
    plan_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      loaded: false,
      title: "Specify Some Provisions",
      subtitle: "Almost done!",
      section_code: "main",
      _stages: [{ label: "Main Provisions", id: "main", active: true }],
      provisions: [],
      error: null,
    };
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(`/selections/plan/${this.plan_id}/provisions`);
    this.provisions = [...res.data];
    this.loaded = true;
  },
  computed: {
    stages() {
      return [
        ...this._stages.map((stg) => {
          return { ...stg, active: stg.id === this.section_code };
        }),
      ];
    },
    output() {
      return this.provisions.map((item) => {
        const val = this.convertDataType(item.ui_provision_value);
        const data = {
          selection_plan_id: this.plan_id,
          config_provision_id: item.config_provision_id,
          provision_value: String(val),
          provision_data_type: typeof val,
        };
        if (item.selection_provision_id) {
          data.selection_provision_id = item.selection_provision_id;
        }
        return data;
      });
    },
  },
  methods: {
    convertDataType(val) {
      if (["true", "false"].includes(val.toLowerCase())) {
        return val.toLowerCase() === "true";
      }
      if (!isNaN(+val)) {
        return +val;
      }
      return val;
    },
    routeTo(route_name, query = {}) {
      this.$router.push({
        name: route_name,
        params: { plan_id: this.plan_id },
        query: { ...query },
      });
    },

    async save() {
      const res = await axios.post(
        `/selections/plan/${this.plan_id}/provisions`,
        this.output
      );

      await axios.post(`/selections/plan/${this.plan_id}/rates`);
      this.routeTo("home");
    },
  },
};
</script>

<style scoped></style>
