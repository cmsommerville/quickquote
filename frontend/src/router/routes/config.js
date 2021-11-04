import ConfigProductList from "../../views/config/ConfigProductList";
import ConfigProduct from "../../views/config/ConfigProduct";
import ConfigFactor from "../../views/config/ConfigFactor.vue";
import ConfigProvision from "../../views/config/ConfigProvision.vue";
import ConfigProvisionList from "../../views/config/ConfigProvisionList.vue";
import ConfigProvisionStates from "../../views/config/ConfigProvisionStates.vue";

export default [
  {
    path: "/config/products",
    name: "config-product-list",
    component: ConfigProductList,
  },
  {
    path: "/config/product/:productId",
    name: "config-product",
    component: ConfigProduct,
  },
  {
    path: "/config/:productId/provisions",
    name: "config-provision-list",
    component: ConfigProvisionList,
  },
  {
    path: "/config/:productId/provision",
    name: "config-provision",
    component: ConfigProvision,
  },
  {
    path: "/config/:id/provision/states",
    name: "config-provision-states",
    component: ConfigProvisionStates,
  },
  {
    path: "/config/factor",
    name: "config-factor",
    component: ConfigFactor,
  },
];
