<template>
  <div>
    <span
      :class="{
        'brand-name-front': true,
        'secondary--text': dark,
        'primary--text': !dark,
      }"
      >Pi</span
    ><span
      :class="{
        'brand-name-back': true,
        'white--text': dark,
        'accent--text': !dark,
      }"
      >Rate</span
    >
  </div>
</template>

<script>
export default {
  name: "TheLogo",
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.brand-name-front {
  font-weight: 500;
  font-size: 2rem;
  text-transform: lowercase;
  font-family: "Wallpoet", cursive;
}
.brand-name-back {
  font-weight: 200;
  font-size: 2rem;
  text-transform: lowercase;
  font-family: "Wallpoet", cursive;
}

.dummy-fonts {
  font-family: "Griffy", cursive;
  font-family: "Metal Mania", cursive;
  font-family: "Monofett", cursive;
  font-family: "Train One", cursive;
  font-family: "Turret Road", cursive;
  font-family: "Uncial Antiqua", cursive;
  font-family: "Wallpoet", cursive;
}
</style>
