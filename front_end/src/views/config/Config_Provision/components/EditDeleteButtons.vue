<template>
  <div class="flex items-center justify-center h-full">
    <app-button :fab="true" class="p-2 mr-1" @click="editHandler"
      ><pencil-icon class="h-4 w-4"
    /></app-button>
    <app-button :fab="true" class="bg-red-600 p-2" @click="deleteHandler"
      ><x-icon class="w-4 h-4"
    /></app-button>
  </div>
</template>

<script>
import AppModal from "@/components/AppModal.vue";
export default {
  name: "EditDeleteButtons",
  components: { AppModal },
  props: {
    editRuleHandler: {
      required: true,
    },
    deleteRuleHandler: {
      required: true,
    },
  },
  mounted() {
    this.rowData = { ...this.params.data };
  },
  data() {
    return {
      rowData: {},
    };
  },
  methods: {
    editHandler() {
      this.editRuleHandler(this.rowData);
    },
    deleteHandler() {
      this.deleteRuleHandler(this.rowData);
    },
  },
};
</script>

<style></style>
