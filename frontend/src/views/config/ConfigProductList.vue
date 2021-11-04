<template>
  <div>
    <v-item-group mandatory v-model="selectedProductIndex">
      <v-container>
        <v-row>
          <v-col
            v-for="product in products"
            :key="product.name"
            cols="12"
            md="3"
          >
            <v-item v-slot="{ active, toggle }">
              <v-card
                class="d-flex justify-center align-center tile-product"
                :dark="active"
                height="200"
                @click="toggle"
              >
                <v-card-title class="tile-product-title">
                  {{ product.name === "accident" ? "AC" : "CI" }}
                </v-card-title>
              </v-card>
            </v-item>
          </v-col>
        </v-row>
      </v-container>
    </v-item-group>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="editProduct"> Edit </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios.js";

export default {
  name: "ConfigProductList",
  async mounted() {
    const res = await axios.get("/config/plans");
    this.products = [...res.data];
  },
  data() {
    return {
      products: [],
      selectedProductIndex: null,
    };
  },
  computed: {
    selectedProduct() {
      return this.products[this.selectedProductIndex];
    },
  },
  methods: {
    async editProduct() {
      await this.$store.dispatch("initializeConfig", this.selectedProduct._id);
      this.$router.push({
        name: "config-product",
        params: { productId: this.selectedProduct._id },
      });
    },
  },
};
</script>

<style scoped>
.tile-product {
  background-image: linear-gradient(
    to bottom right,
    rgb(198, 71, 71),
    rgb(169, 65, 65)
  );
}

.v-item--active {
  outline: 4px solid rgb(67, 0, 0);
  outline-offset: 2px;
}

.tile-product-title {
  color: rgb(255, 133, 133);
  text-align: center;
  font-size: 7rem;
  font-weight: 200;
}
</style>
