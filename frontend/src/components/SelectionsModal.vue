<template>
  <v-dialog transition="dialog-bottom-transition" max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-speed-dial absolute right bottom direction="top">
        <template v-slot:activator>
          <v-btn color="accent" dark fab v-bind="attrs" v-on="on">
            <v-icon> mdi-pencil </v-icon>
          </v-btn>
        </template>
      </v-speed-dial>
    </template>
    <template v-slot:default="dialog">
      <v-card>
        <v-toolbar color="primary" dark>{{ title }}</v-toolbar>
        <div class="d-flex justify-center align-center">
          <ag-grid-vue
            style="width: 100%; height: 70vh"
            class="ag-theme-material"
            :columnDefs="columnDefs"
            :rowData="rowData"
            @cell-value-changed="onCellValueChanged"
          >
          </ag-grid-vue>
        </div>
        <v-card-actions class="justify-end">
          <v-btn text @click="dialog.value = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import { AgGridVue } from "ag-grid-vue";

function numberParser(params) {
  return Number(params.newValue);
}

export default {
  name: "SelectionsModal",
  props: {
    title: {
      required: true,
      type: String,
    },
    selections: {
      required: true,
      type: Object,
    },
  },
  components: {
    AgGridVue,
  },
  computed: {
    columnDefs() {
      return [
        { headerName: "Benefit Code", field: "name", hide: true },
        { headerName: "Benefit Name", field: "text" },
        {
          headerName: "Selected Amount",
          field: "selectedValue",
          editable: true,
          valueParser: numberParser,
        },
        { headerName: "Unit", field: "unit" },
      ];
    },
    rowData() {
      const benefits = [];
      for (const key in this.selections) {
        benefits.push({
          ...this.selections[key],
          unit: this.selections[key].amounts.unit === "percent" ? "%" : "$",
        });
      }
      return benefits;
    },
  },
  methods: {
    onCellValueChanged(e) {
      const r = this.rowData.find((row) => row.text === e.data.text);
      this.$emit("customized-benefits", { ...r });
    },
  },
};
</script>

<style></style>
