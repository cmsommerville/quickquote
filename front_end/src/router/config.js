import routes_config_product from "@/views/config/Config_Product/routes.js";
import routes_config_product_variations from "@/views/config/Config_ProductVariations/routes.js";
import routes_config_age_bands from "@/views/config/Config_AgeBands/routes.js";
import routes_config_coverages from "@/views/config/Config_Coverage/routes.js";
import routes_config_benefits from "@/views/config/Config_Benefit/routes.js";

export default [
  ...routes_config_product,
  ...routes_config_product_variations,
  ...routes_config_age_bands,
  ...routes_config_coverages,
  ...routes_config_benefits,
];
