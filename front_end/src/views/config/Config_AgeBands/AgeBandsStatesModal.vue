<template>
  <app-modal v-bind="$attrs" @close:modal="$emit('close:modal')">
    <template #header>Add States</template>
    <template #content="contentProps">
      <div class="my-2 gap-8 w-50vw">
        <div class="h-96 flex justify-center">
          <united-states-map
            class="w-full"
            :disabled_states="configured_states"
          />
        </div>
        <div class="my-8 flex justify-center">
          <app-button class="mx-4" @click="save(contentProps.close)"
            >Save</app-button
          >
          <app-button
            class="mx-4"
            @click="toggleAllStates"
            :transparent="true"
            >{{
              selected_states.length > 0 ? "Unselect All" : "Select All"
            }}</app-button
          >
        </div>
      </div></template
    >
    <globe-alt-icon class="h-full w-full" />
  </app-modal>
</template>

<script>
import AppModal from "@/components/AppModal.vue";
import UnitedStatesMap from "@/components/USAMap/USAMap.vue";

export default {
  name: "Config_AgeBandsStates_Modal",
  components: { AppModal, UnitedStatesMap },
  data() {
    return {
      configured_states: [],
    };
  },
  methods: {
    toggleAllStates() {
      this.$store.commit("toggle_all_states");
    },
    async save(callback) {
      this.$emit("add:states", [...this.selected_states]);
      callback();
    },
  },
  computed: {
    selected_states() {
      return this.$store.getters.get_selected_states;
    },
  },
};
</script>

<style></style>
