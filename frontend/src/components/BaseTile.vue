<template>
  <li
    :class="{
      tile: true,
      active: clicked,
    }"
    @click="clickHandler"
  >
    <slot></slot>
  </li>
</template>

<script>
export default {
  name: "BaseTile",
  data() {
    return {
      clicked: false,
    };
  },
  methods: {
    clickHandler() {
      this.clicked = !this.clicked;
    },
  },
};
</script>

<style scoped>
li {
  list-style: none;
}

.tile {
  cursor: pointer;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.active {
  background-image: linear-gradient(
    to left,
    rgba(0, 0, 0, 0.15),
    rgba(0, 0, 0, 0.15)
  );
}
</style>
