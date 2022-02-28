<template>
  <app-modal ref="modal" v-bind="$attrs" @close:modal="$emit('close:modal')">
    <template #header>Edit State</template>
    <template #content>
      <div class="flex flex-col justify-center items-center">
        <div class="grid grid-cols-2 gap-8">
          <div class="mt-8 lg:w-72">
            <app-input v-model="provision_code" :disabled="true">
              Provision Code
            </app-input>
          </div>
          <div class="mt-8 lg:w-72">
            <app-select
              v-model="provision_state.state_id"
              :items="[provision_state]"
              item_text="state_name"
              item_value="state_id"
              :disabled="true"
            >
              State
            </app-select>
          </div>
          <div class="mt-8 lg:w-72">
            <app-input
              type="date"
              v-model="provision_state.state_effective_date"
            >
              Effective Date
            </app-input>
          </div>
          <div class="mt-8 lg:w-72">
            <app-input v-model="provision_state.state_expiration_date">
              Expiration Date
            </app-input>
          </div>
        </div>

        <div class="mt-12 mb-6">
          <app-button @click="save">Save</app-button>
        </div>
      </div>
    </template>
    Edit State
  </app-modal>
</template>

<script>
import axios from "@/services/axios.js";
import AppModal from "@/components/AppModal.vue";
import { Model_ConfigProvisionState } from "@/models/Model_ConfigProvision.js";

export default {
  name: "Config_EditProvisionStatesModal",
  components: { AppModal },
  props: {
    provision_state: {
      required: true,
      type: Object,
    },
    provision_code: {
      required: true,
      type: String,
    },
  },
  methods: {
    modelSetter(data) {
      return new Model_ConfigProvisionState(
        data.provision_state_id,
        data.provision_id,
        data.state_id,
        data.state_effective_date,
        data.state_expiration_date
      );
    },
    open() {
      this.$refs.modal.openHandler();
    },
    async save() {
      try {
        await axios.put(
          `/config/provision/state/${this.output.provision_state_id}`,
          this.output
        );
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Updated provision");
        this.$refs.modal.closeHandler();
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
  computed: {
    output() {
      return this.modelSetter(this.provision_state);
    },
  },
};
</script>

<style></style>
