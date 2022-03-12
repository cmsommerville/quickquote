import { roundToNearestMinutes } from "date-fns/esm";

export const CONFIG_AGE_DISTRIBUTION_LIST__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "age_distribution_set_id",
    width: 90,
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Label",
    field: "age_distribution_set_label",
    width: 500,
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "# Ages Configured",
    field: "age_count",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Average Age",
    field: "average_age",
    sortable: true,
    filter: true,
    resizable: true,
  },
];

export const CONFIG_AGE_DISTRIBUTION__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "age_distribution_id",
    width: 90,
    sortable: true,
    filter: true,
    resizable: true,
    valueFormatter: (params) => {
      if (params.value == null) {
        return "-";
      }
    },
  },
  {
    headerName: "Age",
    field: "age",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Weight",
    field: "weight",
    sortable: true,
    filter: true,
    resizable: true,
    editable: true,
  },
];

export const CONFIG_SMOKER_STATUS_DISTRIBUTION_LIST__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "attr_distribution_set_id",
    width: 90,
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Label",
    field: "attr_distribution_set_label",
    width: 500,
    sortable: true,
    filter: true,
    resizable: true,
  },
];

export const CONFIG_SMOKER_STATUS_DISTRIBUTION__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "attr_distribution_id",
    width: 90,
    sortable: true,
    filter: true,
    resizable: true,
    valueFormatter: (params) => {
      if (params.value == null) {
        return "-";
      }
    },
  },
  {
    headerName: "Smoker Status",
    field: "attr_value",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Weight",
    field: "weight",
    sortable: true,
    filter: true,
    resizable: true,
    editable: true,
  },
];

export const CONFIG_GENDER_DISTRIBUTION_LIST__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "attr_distribution_set_id",
    width: 90,
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Label",
    field: "attr_distribution_set_label",
    width: 500,
    sortable: true,
    filter: true,
    resizable: true,
  },
];

export const CONFIG_GENDER_DISTRIBUTION__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "attr_distribution_id",
    width: 90,
    sortable: true,
    filter: true,
    resizable: true,
    valueFormatter: (params) => {
      if (params.value == null) {
        return "-";
      }
    },
  },
  {
    headerName: "Gender",
    field: "attr_value",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Weight",
    field: "weight",
    sortable: true,
    filter: true,
    resizable: true,
    editable: true,
  },
];
