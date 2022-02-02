<template>
  <div>
    <h2>This is the root page</h2>
    <router-view :variations="variations"></router-view>
  </div>
</template>

<script>
export default {
  name: "TestRoot",
  data() {
    return {
      variations: ["A", "B"],
    };
  },
};
</script>

<style></style>
