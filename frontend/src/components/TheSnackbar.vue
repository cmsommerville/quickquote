<template>
  <v-snackbar
    v-model="_snackbar"
    :timeout="5000"
    class="text-uppercase font-weight-black"
  >
    {{ snackbar_message }}

    <template v-slot:action="{ attrs }">
      <v-btn color="secondary" text v-bind="attrs" @click="_snackbar = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  name: "TheSnackbar",
  props: {
    snackbar: {
      default: false,
      type: Boolean,
    },
    snackbar_message: {
      default: "",
    },
  },
  computed: {
    _snackbar: {
      get() {
        return this.snackbar;
      },
      set(val) {
        if (!val) {
          this.$store.commit("INITIALIZE_SNACKBAR");
        }
      },
    },
  },
};
</script>
