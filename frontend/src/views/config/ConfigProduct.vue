<template>
  <div>
    <div class="mb-4" v-if="loaded">
      <v-row>
        <v-col></v-col>
        <v-col sm="4">
          <v-text-field v-model="label" filled outlined label="Product Name" />
        </v-col>
        <v-col></v-col>
        <v-col sm="4">
          <v-text-field v-model="code" filled outlined label="Product Code" />
        </v-col>
        <v-col></v-col>
      </v-row>
      <v-row>
        <v-col sm="6" class="d-flex flex-column">
          <v-row>
            <v-col sm="12">
              <app-dashboard-card
                title="Variations"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureVariations"
              >
                {{
                  config && config.variations
                    ? `${config.variations.length} variations configured`
                    : "Setup Variations!"
                }}
              </app-dashboard-card>
            </v-col>
          </v-row>
          <v-row>
            <v-col sm="12">
              <app-dashboard-card
                title="States"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureStates"
              >
                {{
                  config && config.statesApproved
                    ? `${config.statesApproved.length} states configured`
                    : "Setup States!"
                }}
              </app-dashboard-card>
            </v-col>
          </v-row>
        </v-col>

        <v-col sm="6" class="d-flex flex-column">
          <v-row>
            <v-col sm="12">
              <app-dashboard-card
                title="Benefits"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureBenefits"
              >
                {{
                  config && config.benefits
                    ? `${config.benefits.length} benefits configured`
                    : "Setup Benefits!"
                }}
              </app-dashboard-card>
            </v-col>
          </v-row>

          <v-row>
            <v-col sm="12">
              <app-dashboard-card
                title="Provisions"
                img="https://upload.wikimedia.org/wikipedia/commons/1/1a/Blank_US_Map_%28states_only%29.svg"
                @click:configure="configureProvisions"
              >
                {{
                  config && config.provisions
                    ? `${config.provisions.length} provisions`
                    : "Setup Provisions!"
                }}
              </app-dashboard-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="saveProduct"> Save </v-btn>
    </div>
  </div>
</template>

<script>
// import AppModalListForm from "../../components/AppModalListForm.vue";
import AppDashboardCard from "../../components/AppDashboardCard.vue";

export default {
  name: "ConfigProduct",
  components: { AppDashboardCard },
  async mounted() {
    this.loaded = false;
    const config = await this.$store.getters.getConfig;
    this.config = { ...config };
    this.label = config.text;
    this.code = config.name;
    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      config: null,
      label: null,
      code: null,
    };
  },
  computed: {},
  methods: {
    routeToProvisionList() {
      this.$router.push({
        name: "config-provision-list",
        params: {
          productId: this.config._id,
        },
      });
    },
    saveProduct() {},
    configureProvisions() {
      this.routeToProvisionList();
    },
    configureBenefits() {
      console.log("Configure benefits");
    },
    configureStates() {
      console.log("Configure states!");
    },
    configureVariations() {
      console.log("Configure variations!");
    },
  },
};
</script>

<style>
.card-state {
  position: relative;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
