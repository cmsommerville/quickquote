<template>
  <div>
    <p>This is the Page 1</p>
    {{ variations }}
  </div>
</template>

<script>
export default {
  name: "TestPage1",
  props: {
    variations: {
      type: Array,
    },
  },
};
</script>

<style></style>
