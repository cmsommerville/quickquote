import axios from "@/services/axios.js";

export const FACTOR_OBJECTS = [
  {
    class_code: "plan",
    class_name: "Plan",
    fields: [
      {
        field_code: "plan_effective_date",
        field_name: "Plan Effective Date",
        field_value_data_type: "string",
      },
      {
        field_code: "rating_state",
        field_name: "Rating State",
        field_value_list: async () => {
          const res = await axios.get(`/config/ref-states?all=N`);
          return res.data.map((state) => {
            return { label: state.state_name, code: state.state_code };
          });
        },
        field_value_data_type: "string",
      },
    ],
  },
  {
    class_code: "rate_table",
    class_name: "Rate Table",
    fields: [
      {
        field_code: "age",
        field_name: "Age",
        field_value_data_type: "number",
      },
      {
        field_code: "gender",
        field_name: "Gender",
        field_value_list: () => {
          return [
            { label: "Male", code: "M" },
            { label: "Female", code: "F" },
          ];
        },
        field_value_data_type: "string",
      },
      {
        field_code: "smoker_status",
        field_name: "Smoker Status",
        field_value_list: () => {
          return [
            { label: "Non-Smoker", code: "N" },
            { label: "Smoker", code: "S" },
          ];
        },
        field_value_data_type: "string",
      },
    ],
  },
];
