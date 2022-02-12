<template>
  <app-modal v-bind="$attrs" @close:modal="$emit('close:modal')">
    <template #header>Edit State</template>
    <template #content>
      <div class="flex flex-col justify-center items-center">
        <div class="grid grid-cols-2 gap-8">
          <div class="mt-8 lg:w-72">
            <app-input v-model="benefit.benefit_code" :disabled="true">
              Benefit Code
            </app-input>
          </div>
          <div class="mt-8 lg:w-72">
            <app-select
              v-model="benefit.state_id"
              :items="[benefit.state]"
              item_text="state_name"
              item_value="state_id"
              :disabled="true"
            >
              State
            </app-select>
          </div>
          <div class="mt-8 lg:w-72">
            <app-input type="date" v-model="benefit.benefit_effective_date">
              Effective Date
            </app-input>
          </div>
          <div class="mt-8 lg:w-72">
            <app-input v-model="benefit.benefit_expiration_date">
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
import { Model_ConfigBenefitState } from "@/models/Model_ConfigBenefit.js";

export default {
  name: "Config_EditBenefitStatesModal",
  components: { AppModal },
  props: {
    benefit: {
      required: true,
      type: Object,
    },
  },
  methods: {
    modelSetter(data) {
      return new Model_ConfigBenefitState(
        data.parent_id,
        data.product_id,
        data.state_id,
        data.benefit_code,
        data.benefit_effective_date,
        data.benefit_expiration_date
      );
    },
    async save() {
      try {
        const data = {
          ...this.modelSetter(this.benefit),
          benefit_id: this.benefit.benefit_id,
        };
        await axios.put(`/config/benefit/${this.benefit.benefit_id}`, data);
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", "Updated benefit");
      } catch (err) {
        this.$store.dispatch("SET_SNACKBAR_MESSAGE", err);
      }
    },
  },
};
</script>

<style></style>
