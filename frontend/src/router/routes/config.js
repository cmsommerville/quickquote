import ConfigFactor from "../../views/config/ConfigFactor.vue";
import ConfigProvision from "../../views/config/ConfigProvision.vue";
import ConfigProvisionList from "../../views/config/ConfigProvisionList.vue";
import ConfigProvisionStates from "../../views/config/ConfigProvisionStates.vue";

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
    path: "/config/provision/states",
    name: "config-provision-states",
    component: ConfigProvisionStates,
  },
  {
    path: "/config/factor",
    name: "config-factor",
    component: ConfigFactor,
  },
];
