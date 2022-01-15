<template>
  <div class="container">
    <div class="form-rater" v-if="loaded">
      <v-form class="form" @submit="save" @reset="onReset" v-if="show">
        <component
          v-for="provision in provisions"
          :key="provision.provision_id"
          :is="provision.ui_component.component_type_code"
          v-bind="{ ...provision.ui_component }"
          :name="provision.provision_code"
          v-model="provision.ui_provision_value"
        />

        <div class="d-flex justify-center my-3">
          <v-btn depressed color="primary" type="submit" class="mx-3">
            Submit
          </v-btn>

          <v-btn depressed color="secondary" class="mx-3"> Reset </v-btn>
        </div>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";
import { VTextField, VSelect, VSwitch } from "vuetify/lib";

export default {
  name: "Provisions",
  props: {
    plan_id: {
      type: [Number, String],
      required: true,
    },
  },
  components: {
    VSelect,
    VTextField,
    VSwitch,
  },
  data() {
    return {
      loaded: false,
      provisions: [],
      show: true,
    };
  },
  computed: {
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
  async mounted() {
    this.loaded = false;
    const res = await axios.get(`/selections/plan/${this.plan_id}/provisions`);
    this.provisions = [...res.data];
    this.loaded = true;
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
    async save(event) {
      event.preventDefault();
      const res = await axios.post(
        `/selections/plan/${this.plan_id}/provisions`,
        this.output
      );
      this.mergeSelections(res.data);

      await axios.post(`/selections/plan/${this.plan_id}/rates`);
      this.routeTo("rating-premium");
    },
    mergeSelections(data) {
      this.provisions = [
        ...this.provisions.map((prov) => {
          const sel_index = data.findIndex(
            (item) => item.config_provision_id === prov.config_provision_id
          );
          return {
            ...prov,
            selection_provision_id:
              sel_index < 0 ? null : data[sel_index].selection_provision_id,
          };
        }),
      ];
    },
    onReset(event) {
      event.preventDefault();
      console.log(this.selectionSubmissionHandler());
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-rater {
  min-width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}
</style>
