<template>
  <v-item-group v-model="selected_config" @change="changeHandler">
    <v-container>
      <v-row>
        <v-col v-for="product in config" :key="product.name" cols="12" md="6">
          <v-item v-slot="{ active, toggle }" :value="product">
            <v-card
              :color="active ? 'accent' : 'secondary'"
              class="d-flex align-center"
              height="100"
              @click="toggle"
            >
              <div
                :class="`text-h4 flex-grow-1 text-center ${
                  active ? 'white--text' : ''
                }`"
              >
                {{ product.text }}
              </div>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script>
export default {
  name: "TileListGroup",
  props: {
    config: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selected_config: {},
    };
  },
  methods: {
    changeHandler() {
      this.$emit("tile:selected", this.selected_config);
    },
  },
};
</script>

<style></style>
