<template>
  <app-modal ref="modal" v-bind="$attrs" @close:modal="$emit('close:modal')">
    <template #header>Add States</template>
    <template #content>
      <div class="my-2 grid grid-cols-3 gap-8">
        <div class="col-span-2">
          <div class="h-96 flex justify-center">
            <united-states-map
              class="w-full"
              :disabled_states="configured_states"
            />
          </div>
          <div class="flex justify-center mt-2">
            <app-button
              class="h-10 text-xs"
              @click="toggleAllStates"
              :transparent="true"
              >{{
                selected_states.length > 0 ? "Unselect All" : "Select All"
              }}</app-button
            >
          </div>
        </div>
        <div class="flex flex-col justify-center items-center">
          <div class="my-8">
            <app-input type="date" v-model="effective_date"
              >Effective Date</app-input
            >
          </div>
          <div class="my-8">
            <app-input type="date" v-model="expiration_date"
              >Expiration Date</app-input
            >
          </div>
          <div class="my-8">
            <app-button @click="save">Save</app-button>
          </div>
        </div>
      </div></template
    >
    <globe-alt-icon class="h-6 w-6" />
  </app-modal>
</template>

<script>
import axios from "@/services/axios.js";
import AppModal from "@/components/AppModal.vue";
import UnitedStatesMap from "@/components/USAMap/USAMap.vue";
import { Model_ConfigProvisionState } from "@/models/Model_ConfigProvision.js";

export default {
  name: "Config_NewProvisionStates_Modal",
  components: { AppModal, UnitedStatesMap },
  props: {
    provision: {
      required: true,
      type: Object,
    },
  },
  mounted() {
    this.effective_date = this.provision.provision_effective_date;
    this.expiration_date = this.provision.provision_expiration_date;
    this.configured_states = [...this.provision.states];
  },
  data() {
    return {
      effective_date: "1900-01-01",
      expiration_date: "9999-12-31",
      configured_states: [],
    };
  },
  methods: {
    open() {
      this.$refs.modal.openHandler();
    },
    toggleAllStates() {
      this.$store.commit("toggle_all_states");
    },
    async save() {
      try {
        const res = await axios.post("/config/provision/states", this.output);
        this.$store.dispatch(
          "SET_SNACKBAR_MESSAGE",
          `Added ${res.data.length} states!`
        );
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
  computed: {
    selected_states() {
      return this.$store.getters.get_selected_states;
    },
    output() {
      return this.selected_states.map((st) => {
        return new Model_ConfigProvisionState(
          null,
          this.provision.provision_id,
          st.state_id,
          this.effective_date,
          this.expiration_date
        );
      });
    },
  },
};
</script>

<style></style>
