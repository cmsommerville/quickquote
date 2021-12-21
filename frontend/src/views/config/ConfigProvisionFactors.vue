<template>
  <div class="container">
    <div class="content">
      <v-list>
        <v-list-item v-for="(factor, ix) in factors" :key="ix">
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
                  >Factor Value: {{ factor.factor_value }}</span
                >
              </v-chip>
              <v-chip
                v-for="(rule, key) in factor.factor_rules"
                :key="key"
                class="mr-2 my-1"
              >
                {{ ruleDisplayHandler(rule) }}
              </v-chip>
            </div>
          </v-card>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>

      <div>
        <v-btn @click="save" color="primary" class="mx-4"> Save Factor </v-btn>
        <factor-config-modal @submit:factor-config="addConditionToRuleArray">
          Add Rule
        </factor-config-modal>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";
import { OPERATORS } from "../../data/lookups.js";
import FactorConfigModal from "../../components/FactorConfigModal.vue";

export default {
  name: "ConfigFactor",
  components: { FactorConfigModal },
  props: {
    product_id: {
      type: [Number, String],
      required: true,
    },
    provision_id: {
      type: [Number, String],
      required: true,
    },
  },
  data() {
    return {
      loaded: false,
      factors: [],
      factor_value: null,
    };
  },
  async mounted() {
    this.loaded = false;
    const res_factors = axios.get(
      `/qry-config/factors?provision_id=${this.provision_id}`
    );
    this.factors = await [...res_factors.data];
    this.loaded = true;
  },
  computed: {
    output() {
      return this.factors.map((factor) => {
        return {
          ...factor,
          provision_id: this.provision_id,
        };
      });
    },
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        query: { product_id: this.product_id, provision_id: this.provision_id },
        params: { ...params },
      });
    },
    addConditionToRuleArray(payload) {
      const { factor_value, rules } = payload;
      this.factors = [...this.factors, { factor_value, factor_rules: rules }];
    },
    ruleDisplayHandler(rule) {
      const operators = { ...OPERATORS };
      return `${rule.field_name} ${operators[rule.comparison_operator_code]} ${
        rule.field_value
      }`;
    },
    async save() {
      await axios.post("/config/factor", this.output);
      // this.routeTo("config-provision", { provision_id: this.provision_id });
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
