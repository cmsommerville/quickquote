export const CONFIG_PROVISION_LIST__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "provision_id",
    width: 90,
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Provision Code",
    field: "provision_code",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Provision Name",
    field: "provision_label",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "# States Configured",
    field: "state_count",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "# Factors Configured",
    field: "factor_count",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Effective Date",
    field: "provision_effective_date",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Expiration Date",
    field: "provision_expiration_date",
    sortable: true,
    filter: true,
    resizable: true,
  },
];

export const CONFIG_PROVISION_STATES_LIST__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "provision_state_id",
    width: 90,
    sortable: true,
    filter: true,
  },
  {
    headerName: "Provision Code",
    field: "provision_code",
    sortable: true,
    filter: true,
  },
  {
    headerName: "State Code",
    field: "state_code",
    sortable: true,
    filter: true,
  },
  {
    headerName: "Effective Date",
    field: "state_effective_date",
    sortable: true,
    filter: true,
  },
  {
    headerName: "Expiration Date",
    field: "state_expiration_date",
    sortable: true,
    filter: true,
  },
];

export const CONFIG_PROVISION_UI_SELECT_ITEMS__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "ui_component_item_id",
    width: 90,
    sortable: true,
    filter: true,
  },
  {
    headerName: "Item Code",
    field: "item_code",
    sortable: true,
    filter: true,
  },
  {
    headerName: "Item Name",
    field: "item_label",
    sortable: true,
    filter: true,
  },
];

export const CONFIG_FACTOR_LIST__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "factor_id",
    width: 90,
    filter: true,
    resizable: true,
    rowDrag: true,
  },
  {
    headerName: "Priority",
    field: "factor_priority",
    filter: true,
    resizable: true,
  },
  {
    headerName: "Factor Value",
    field: "factor_value",
    filter: true,
    resizable: true,
  },
  {
    headerName: "Rule #1",
    field: "rule1",
    filter: true,
    resizable: true,
  },
  {
    headerName: "Rule #2",
    field: "rule2",
    filter: true,
    resizable: true,
  },
  {
    headerName: "Rule #3",
    field: "rule3",
    filter: true,
    resizable: true,
  },
];

export const CONFIG_FACTOR_RULE_LIST__COLUMN_DEFS = [
  {
    headerName: "ID",
    field: "factor_rule_id",
    width: 90,
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Class Name",
    field: "class_name",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Field Name",
    field: "field_name",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Operator",
    field: "comparison_operator_symbol",
    sortable: true,
    filter: true,
    resizable: true,
  },
  {
    headerName: "Field Value",
    field: "field_value",
    sortable: true,
    filter: true,
    resizable: true,
  },
];
