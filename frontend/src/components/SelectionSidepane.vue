<template>
  <v-card class="mx-auto selection-pane">
    <v-navigation-drawer permanent>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            <slot>Selections</slot>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-item
          v-for="selection in selections"
          :key="selection.name"
          class="selection-pane-list-item grey--text"
          style="min-height: inherit"
        >
          <v-list-item-content>
            <v-list-item-title>{{ selection.text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-card>
</template>

<script>
export default {
  name: "SelectionSidepane",
  props: {
    selections: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style>
.selection-pane {
  position: fixed;
  right: 10px;
  top: 80px;
  height: 450px;
}

.selection-pane-list-item {
  min-height: 24px;
  max-height: 24px;
}
</style>
