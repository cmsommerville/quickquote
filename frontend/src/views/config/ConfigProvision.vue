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

          <v-row>
            <v-col :sm="ui.component === 'v-select' ? 9 : 12">
              <v-select
                v-model="ui.component"
                filled
                outlined
                label="Component Type"
                :items="componentTypes"
                item-text="label"
                item-value="code"
              />
            </v-col>
            <v-col v-if="ui.component === 'v-select'" sm="3">
              <app-modal-list-form
                v-if="ui.component === 'v-select'"
                title="Select Options"
                :schema="[
                  { code: 'text', label: 'Label' },
                  { code: 'value', label: 'Value' },
                ]"
                @submit:list-data="selectListItemsHandler"
                class="ma-2"
              >
                <v-icon>mdi-pencil-outline</v-icon>
              </app-modal-list-form>
            </v-col>
          </v-row>

          <v-select
            v-if="ui.component === 'v-text-field'"
            v-model="ui.type"
            filled
            outlined
            label="Input Type"
            :items="inputTypes"
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
      <v-col sm="8" class="config-states">
        <v-list-item v-for="state in states" :key="state.code" dense>
          <v-row>
            <v-col sm="2" class="d-flex justify-center align-self-start">
              <v-list-item-content>
                <v-list-item-title class="text-right">{{
                  state.label
                }}</v-list-item-title>
              </v-list-item-content>
            </v-col>
            <v-col sm="3" class="d-flex justify-center align-self-start">
              <v-select
                :items="requirementTypes"
                item-text="label"
                item-value="code"
                v-model="state.value"
                filled
                outlined
                dense
              ></v-select>
            </v-col>

            <v-col sm="3" class="d-flex justify-center align-self-start">
              <v-text-field
                v-model="state.effectiveDate"
                filled
                outlined
                dense
                :disabled="state.value && state.value === 'prohibited'"
                type="date"
                label="Effective Date"
              />
            </v-col>

            <v-col sm="3" class="d-flex justify-center align-self-start">
              <v-text-field
                v-model="state.expiryDate"
                filled
                outlined
                dense
                :disabled="state.value && state.value === 'prohibited'"
                type="date"
                label="Expiry Date"
              />
            </v-col>
          </v-row>
        </v-list-item>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import AppModalListForm from "../../components/AppModalListForm.vue";

export default {
  name: "ConfigProvision",
  components: { AppModalListForm },
  async mounted() {
    const code = this.$route.query.code;
    if (code) {
      const prov = this.$store.getters.getProvisionConfig.find(
        (item) => item.name === code
      );
      if (prov) {
        this.config = { ...prov };
        this.label = prov.label;
        this.name = prov.name;
        this.ui = { ...prov.ui };
        this.states = prov.statesApproved ? prov.statesApproved : this.states;
      }
    }
  },
  data() {
    return {
      modal: false,
      config: null,
      label: null,
      name: null,
      ui: {},
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
        { code: "v-switch", label: "Switch" },
      ],
      inputTypes: [
        { code: "text", label: "Text" },
        { code: "number", label: "Number" },
        { code: "date", label: "Date" },
        { code: "email", label: "Email" },
        { code: "password", label: "Password" },
      ],
    };
  },
  computed: {
    outputProvision() {
      return {
        ...this.config,
        label: this.label,
        name: this.name,
        ui: { ...this.ui },
        statesApproved: this.states,
      };
    },
  },
  methods: {
    submitProvision() {
      this.$store.commit("SET_PROVISION_CONFIG", [this.outputProvision]);
      this.$router.push({ name: "config-provision-list" });
    },
    selectListItemsHandler(payload) {
      this.ui.items = [...payload];
    },
  },
};
</script>

<style>
.config-states {
  border-left: 1px solid #ddd;
}
</style>
