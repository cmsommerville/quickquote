<template>
  <div>
    <template v-if="product_id">
      <config-existing-product :product_id="product_id" />
    </template>

    <template v-else>
      <config-new-product />
    </template>
  </div>
</template>

<script>
import ConfigExistingProduct from "./Config_ExistingProduct.vue";
import ConfigNewProduct from "./Config_NewProduct.vue";

export default {
  name: "Config_Product",
  components: { ConfigExistingProduct, ConfigNewProduct },
  props: {
    product_id: {
      required: false,
      type: [Number, String],
    },
  },
};
</script>
