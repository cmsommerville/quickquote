import Config_DistributionLanding from "./Config_DistributionLanding.vue";
import Config_AgeDistributionList from "./Config_AgeDistributionList.vue";
import Config_SmokerDistributionList from "./Config_SmokerDistributionList.vue";
import Config_GenderDistributionList from "./Config_GenderDistributionList.vue";

export default [
  {
    path: "/config/distributions",
    name: "config-distribution-list",
    component: Config_DistributionLanding,
    props: true,
  },
  {
    path: "/config/distributions/age",
    name: "config-age-distribution-list",
    component: Config_AgeDistributionList,
    props: true,
  },
  {
    path: "/config/distributions/smoker",
    name: "config-smoker-status-distribution-list",
    component: Config_SmokerDistributionList,
    props: true,
  },
  {
    path: "/config/distributions/gender",
    name: "config-gender-distribution-list",
    component: Config_GenderDistributionList,
    props: true,
  },
];
