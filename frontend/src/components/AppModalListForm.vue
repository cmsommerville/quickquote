<template>
  <!-- <div class="text-center"> -->
  <v-dialog v-model="modal" width="700">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="red lighten-2" dark v-bind="attrs" v-on="on">
        <slot>Configure</slot>
      </v-btn>
    </template>

    <v-card>
      <v-card-title class="text-h5 grey lighten-2">
        {{ title }}
      </v-card-title>

      <v-card-text class="mt-4">
        <v-row v-for="(d, i) in data" :key="i">
          <v-col
            v-for="item in schema"
            :key="item.code"
            :sm="item.cols || 12 / schema.length"
          >
            <v-text-field
              filled
              outlined
              dense
              :label="item.label"
              v-model="d[item.code]"
            />
          </v-col>
        </v-row>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="addItem"> Add Item </v-btn>
        <v-btn color="primary" text @click="clickHandler"> Save </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <!-- </div> -->
</template>

<script>
export default {
  name: "AppModalListForm",
  props: {
    title: {
      type: String,
      required: true,
    },
    schema: {
      type: Array,
      required: true,
    },
    inputData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      modal: false,
      data: [],
      newValue: {},
    };
  },
  mounted() {
    if (this.inputData.length > 0) {
      this.data = [...this.inputData];
    } else {
      this.data = [{}];
    }
  },
  methods: {
    clickHandler() {
      this.$emit("submit:list-data", this.data);
      this.modal = !this.modal;
    },
    addItem() {
      if (this.newValue) {
        this.data.push({});
      }
    },
  },
};
</script>

<style></style>
