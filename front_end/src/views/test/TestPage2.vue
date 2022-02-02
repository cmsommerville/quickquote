<template>
  <div>
    <p>This is the Page 2</p>
    {{ variations }}
  </div>
</template>

<script>
export default {
  name: "TestPage2",
  props: {
    variations: {
      type: Array,
    },
  },
};
</script>

<style></style>
