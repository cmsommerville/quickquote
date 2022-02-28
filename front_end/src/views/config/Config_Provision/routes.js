import Config_ProvisionList from "./Config_ProvisionList.vue";
import Config_EditProvisionLanding from "./Config_EditProvisionLanding.vue";
import Config_Provision from "./Config_Provision.vue";
import Config_ProvisionStatesList from "./Config_ProvisionStatesList.vue";
import Config_ProvisionUI from "./Config_ProvisionUI.vue";
import Config_FactorList from "./Config_FactorList.vue";
import Config_Factor from "./Config_Factor.vue";

export default [
  {
    path: "/config/product/:product_id/provisions",
    name: "config-provision-list",
    component: Config_ProvisionList,
    props: true,
  },
  {
    path: "/config/product/:product_id/provision/:provision_id",
    name: "config-provision-landing",
    component: Config_EditProvisionLanding,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/base",
    name: "config-provision-edit",
    component: Config_Provision,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/provision",
    name: "config-provision-new",
    component: Config_Provision,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/states",
    name: "config-provision-states",
    component: Config_ProvisionStatesList,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/ui",
    name: "config-provision-ui",
    component: Config_ProvisionUI,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/factors",
    name: "config-factor-list",
    component: Config_FactorList,
    props: (route) => ({ ...route.params, ...route.query }),
  },
  {
    path: "/config/product/:product_id/provision/:provision_id/factor",
    name: "config-factor",
    component: Config_Factor,
    props: (route) => ({ ...route.params, ...route.query }),
  },
];
