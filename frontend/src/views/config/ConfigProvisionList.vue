<template>
  <div class="content" v-if="provisions">
    <v-row v-for="prov in provisions" :key="prov.name">
      <v-col cols="12" xs="12">
        <v-card class="d-flex justify-space-between">
          <div class="card-content">
            <v-card-title>{{ prov.label }}</v-card-title>
            <v-card-subtitle
              >Component Type: {{ prov.component }}</v-card-subtitle
            >
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
                  @click="editProvision(prov.name)"
                  ><v-icon color="primary">mdi-pencil</v-icon></v-btn
                >
              </template>
              <span>Edit Provision</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  elevation="2"
                  fab
                  x-small
                  class="mr-2"
                  v-bind="attrs"
                  v-on="on"
                  :to="{
                    name: 'config-factor',
                    query: { code: prov.name },
                  }"
                  ><v-icon color="primary"
                    >mdi-file-percent-outline</v-icon
                  ></v-btn
                >
              </template>
              <span>Edit Factors</span>
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
        :to="{ name: 'config-provision' }"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
  </div>
</template>

<script>
export default {
  name: "ConfigProvisionList",
  data() {
    return {
      provisions: null,
    };
  },
  async mounted() {
    const productUUID = "615ba44644247be1d00ab650"; //"6129a7640fb263f14aaa2d5e";
    if (this.$store.getters.isConfigEmpty) {
      await this.$store.dispatch("initializeBaseProductConfig", productUUID);
    }
    this.provisions = [...this.$store.getters.getProvisionConfigList];
  },
  methods: {
    editProvision(code) {
      this.$store.commit(
        "SET_NEW_PROVISION_CONFIG",
        this.provisions.find((item) => item.name === code)
      );
      this.$router.push({
        name: "config-provision",
        query: { code: code },
      });
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
