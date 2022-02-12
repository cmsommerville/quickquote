<template>
  <transition name="slide-up">
    <div
      v-if="message"
      class="_snackbar fixed bottom-0 left-1/2 -translate-x-1/2 w-96 h-16 text-white uppercase text-center flex justify-center items-center rounded-md bg-gradient-to-br from-violet-600 to-indigo-600"
    >
      {{ message }}
    </div>
  </transition>
</template>

<script>
export default {
  name: "AppSnackbar",
  computed: {
    message() {
      return this.$store.getters.get_snackbar_message;
    },
  },
};
</script>

<style>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  height: 0;
  opacity: 0;
}

._snackbar {
  z-index: 999;
}
</style>
