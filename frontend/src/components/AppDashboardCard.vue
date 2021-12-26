<template>
  <v-card class="elevation-4 rounded-sm d-flex justify-space-between">
    <div>
      <v-card-actions>
        <v-btn
          text
          color="primary"
          @click="$emit('click:configure')"
          :disabled="disabled"
        >
          {{ title }}
        </v-btn>
      </v-card-actions>
      <v-card-subtitle class="text-uppercase text-overline">
        <slot></slot>
      </v-card-subtitle>
    </div>
    <v-avatar size="120" tile class="mr-1">
      <v-img contain :src="img"></v-img>
    </v-avatar>
  </v-card>
</template>

<script>
export default {
  name: "AppDashboardCard",
  props: {
    title: {
      required: true,
      type: String,
    },
    img: {
      required: true,
      type: String,
    },
    disabled: {
      default: false,
      type: Boolean,
    },
  },
};
</script>

<style></style>
