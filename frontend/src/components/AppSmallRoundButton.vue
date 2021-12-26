<template>
  <div>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          elevation="2"
          fab
          x-small
          v-bind="attrs"
          v-on="on"
          @click="$emit('click:btn')"
          ><v-icon :color="color">{{ icon }}</v-icon></v-btn
        >
      </template>
      <span>{{ tooltip }}</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  name: "AppSmallRoundButton",
  props: {
    color: {
      default: "primary",
      type: String,
    },
    icon: {
      required: true,
      type: String,
    },
    tooltip: {
      required: true,
      type: String,
    },
  },
};
</script>

<style></style>
