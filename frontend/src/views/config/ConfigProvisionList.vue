<template>
  <div class="content" v-if="provisions">
    <v-row v-for="prov in provisions" :key="prov.name">
      <v-col cols="12" xs="12">
        <v-card class="d-flex justify-space-between">
          <div class="card-content">
            <v-card-title>{{ prov.provision.provision_label }}</v-card-title>
            <!-- <v-card-subtitle
              >Component Type: {{ prov.ui.component }}</v-card-subtitle
            > -->
          </div>
          <div class="card-edit-buttons ma-2">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  elevation="2"
                  fab
                  x-small
                  class="mr-2"
                  v-bind="attrs"
                  v-on="on"
                  @click="editProvision(prov.provision_id)"
                  ><v-icon color="primary">mdi-pencil</v-icon></v-btn
                >
              </template>
              <span>Edit Provision</span>
            </v-tooltip>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-fab-transition>
      <v-btn
        color="pink"
        dark
        absolute
        bottom
        fab
        right
        @click="routeTo('config-provision')"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn
        color="primary"
        class="mx-4"
        @click="routeTo('config-product', { product_id })"
      >
        Back to Product
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigProvisionList",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
  },
  data() {
    return {
      provisions: [],
    };
  },
  async mounted() {
    const res = await axios.get(
      `/qry-config/all-provisions?product_id=${this.product_id}`
    );
    this.provisions = [...res.data];
  },
  methods: {
    saveProvisions() {
      console.log("Saved");
    },
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: { product_id: this.product_id },
        query: { ...params },
      });
    },
    editProvision(id) {
      this.routeTo("config-provision", { provision_id: id });
    },
  },
};
</script>

<style scoped>
.content {
  width: 60%;
  border: 1px solid #ddd;
  margin: 2rem auto;
  position: relative;
}
</style>
