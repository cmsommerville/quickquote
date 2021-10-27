import ConfigFactor from "../../views/config/ConfigFactor.vue";
import ConfigProvision from "../../views/config/ConfigProvision.vue";
import ConfigProvisionList from "../../views/config/ConfigProvisionList.vue";

export default [
  {
    path: "/config/provisions",
    name: "config-provision-list",
    component: ConfigProvisionList,
  },
  {
    path: "/config/provision",
    name: "config-provision",
    component: ConfigProvision,
  },
  {
    path: "/config/factor",
    name: "config-factor",
    component: ConfigFactor,
  },
];
