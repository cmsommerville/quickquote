<template>
  <div class="container">
    <div class="content d-flex justify-center align-start">
      <v-row>
        <v-col sm="6">
          <v-form>
            <v-text-field
              v-model="factor_code"
              filled
              outlined
              label="Factor Code"
            />

            <v-text-field
              v-model="factor_name"
              filled
              outlined
              label="Factor Name"
            />

            <v-text-field
              v-model.number="default_factor_value"
              filled
              outlined
              type="number"
              label="Default Factor Value"
            />

            <div class="call-to-action d-flex justify-center align-center">
              <v-btn @click="saveFactorHandler" color="primary" class="mx-4">
                Save Factor
              </v-btn>
              <factor-config-modal
                @submit:factor-config="addConditionToRuleArray"
              >
                Add Rule
              </factor-config-modal>
            </div>
          </v-form>
        </v-col>
        <v-col sm="6">
          <v-list>
            <v-list-item v-for="(item, ix) in rules" :key="ix">
              <v-card
                elevation-1
                width="100%"
                class="
                  mx-auto
                  my-2
                  px-4
                  py-4
                  d-flex
                  justify-space-between
                  align-center
                "
              >
                <div class="factor-card-order">
                  <v-avatar color="secondary" size="48" class="mr-12">
                    <span class="text-h5">{{ ix + 1 }}</span>
                  </v-avatar>
                </div>
                <div class="factor-card-rules text-right">
                  <v-chip color="pink lighten-2 mr-2 my-1">
                    <span class="white--text"
                      >Factor Value: {{ item.factor_value }}</span
                    >
                  </v-chip>
                  <v-chip
                    v-for="(rule, key) in item.rules"
                    :key="key"
                    class="mr-2 my-1"
                  >
                    {{ ruleDisplayHandler(rule) }}
                  </v-chip>
                </div>
              </v-card>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import { OPERATORS } from "../../data/lookups.js";
import FactorConfigModal from "../../components/FactorConfigModal.vue";

export default {
  name: "ConfigFactor",
  components: { FactorConfigModal },
  props: {
    productId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      factor_code: null,
      factor_name: null,
      default_factor_value: 1.0,
      rules: [],
    };
  },
  async mounted() {
    const code = this.$route.query.code;
    if (code) {
      const prov = this.$store.getters.getProvisionConfig;
      this.factor_code = prov.name;
      this.factor_name = prov.label;
      if (prov.factor) {
        this.default_factor_value = prov.factor.default_factor_value;
        this.rules = prov.factor.variability;
      }
    }
  },
  computed: {
    output() {
      return {
        factor_code: this.factor_code,
        default_factor_value: this.default_factor_value,
        variability: this.rules,
      };
    },
  },
  methods: {
    routeToProvision() {
      this.$router.push({
        name: "config-provision",
        query: { code: this.factor_code },
        params: { productId: this.productId },
      });
    },
    addConditionToRuleArray(payload) {
      this.rules = [...this.rules, payload];
    },
    saveFactorHandler() {
      this.$store.commit("SET_PROVISION_FACTORS", this.output);
      this.routeToProvision();
    },
    ruleDisplayHandler(rule) {
      const operators = { ...OPERATORS };
      if (["range", "nrange"].includes(rule.comparison)) {
        return `${rule.label} ${operators[rule.comparison]} ${rule.value} and ${
          rule.upper
        }`;
      }
      return `${rule.label} ${operators[rule.comparison]} ${rule.value}`;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  margin: 2rem auto;
  min-width: 90%;
  border: 1px solid #ddd;
  padding: 2rem;
}

.factor-config-modal {
  width: "500px";
}
</style>
