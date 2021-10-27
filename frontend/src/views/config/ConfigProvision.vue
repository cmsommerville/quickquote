<template>
  <div class="content d-flex justify-center align-start">
    <v-row>
      <v-col sm="4">
        <v-form>
          <v-text-field
            v-model="label"
            filled
            outlined
            label="Provision Name"
          />

          <v-text-field v-model="name" filled outlined label="Provision Code" />

          <v-select
            v-model="component"
            filled
            outlined
            label="Component Type"
            :items="componentTypes"
            item-text="label"
            item-value="code"
          />

          <div class="call-to-action d-flex justify-center align-center">
            <v-btn color="primary" class="mx-4" @click="submitProvision">
              Save
            </v-btn>
          </div>
        </v-form>
      </v-col>
      <v-spacer></v-spacer>
      <v-col sm="7" class="config-states">
        <v-list-item v-for="state in states" :key="state.code" dense>
          <v-row>
            <v-col sm="4" class="d-flex justify-center">
              <v-list-item-content>
                <v-list-item-title class="text-right">{{
                  state.label
                }}</v-list-item-title>
              </v-list-item-content>
            </v-col>
            <v-col sm="8" class="d-flex justify-center">
              <v-radio-group v-model="state.value" row>
                <v-radio
                  v-for="reqType in requirementTypes"
                  :key="reqType.code"
                  :label="reqType.label"
                  :value="reqType.code"
                ></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>
        </v-list-item>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "ConfigProvision",
  async mounted() {
    const code = this.$route.query.code;
    if (code) {
      const prov = this.$store.getters.getProvisionConfig.find(
        (item) => item.name === code
      );
      if (code) {
        this.label = prov.label;
        this.name = prov.name;
        this.component = prov.component;
        this.states = prov.statesApproved ? prov.statesApproved : this.states;
      }
    }
  },
  data() {
    return {
      label: null,
      name: null,
      component: null,
      states: [
        { label: "Alabama", code: "AL", value: "permitted" },
        { label: "Alaska", code: "AK", value: "mandatory" },
        { label: "Arizona", code: "AZ", value: "prohibited" },
        { label: "Arkansas", code: "AR", value: "permitted" },
        { label: "North Carolina", code: "NC", value: "permitted" },
        { label: "South Carolina", code: "SC", value: "permitted" },
      ],
      requirementTypes: [
        { code: "permitted", label: "Permitted" },
        { code: "prohibited", label: "Prohibited" },
        { code: "mandatory", label: "Mandatory" },
      ],

      componentTypes: [
        { code: "v-text-field", label: "Input" },
        { code: "v-select", label: "Select" },
        { code: "v-checkbox", label: "Checkbox" },
        { code: "v-radio", label: "Radio" },
        { code: "v-slider", label: "Slider" },
      ],
    };
  },
  computed: {
    outputProvision() {
      return {
        label: this.label,
        name: this.name,
        component: this.component,
        statesApproved: this.states,
      };
    },
  },
  methods: {
    submitProvision() {
      this.$store.commit("SET_PROVISION_CONFIG", [this.outputProvision]);
      this.$router.push({ name: "config-provision-list" });
    },
  },
};
</script>

<style>
.config-states {
  border-left: 1px solid #ddd;
}
</style>
