<template>
  <div class="container">
    <div class="content" v-if="loaded">
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
            <div class="text-right d-flex justify-center">
              <div class="factor-card-rules">
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
              <div class="card-buttons ml-6 d-flex">
                <div class="buttons d-flex flex-column">
                  <app-small-round-button
                    tooltip="Edit"
                    icon="mdi-pencil"
                    class="ma-1"
                    @click:btn="editRules(ix)"
                  />
                  <app-small-round-button
                    tooltip="Delete"
                    icon="mdi-close"
                    color="pink lighten-1"
                    class="ma-1"
                    @click:btn="deleteFactor(ix)"
                  />
                </div>
                <div class="buttons d-flex flex-column">
                  <app-small-round-button
                    class="ma-1"
                    tooltip="Move Up in Priority"
                    icon="mdi-arrow-up"
                    color="accent"
                    @click:btn="moveRule(ix, -1)"
                  />
                  <app-small-round-button
                    class="ma-1"
                    tooltip="Move Down in Priority"
                    icon="mdi-arrow-down"
                    color="accent"
                    @click:btn="moveRule(ix, 1)"
                  />
                </div>
              </div>
            </div>
          </v-card>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>

      <div>
        <v-btn @click="save" color="primary" class="mx-4"> Save Factor </v-btn>
        <!-- <v-btn @click="addNewRule" dark color="red lighten-2" class="mx-4">
          Add Rule
        </v-btn> -->
        <v-btn color="accent" @click.stop="editRules">Add Rule</v-btn>
        <factor-config-modal
          v-model="dialog"
          :input_data="dialog_input"
          @submit:factor-config="updateRuleArray"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";
import { OPERATORS } from "../../data/lookups.js";
import FactorConfigModal from "../../components/FactorConfigModal.vue";
import AppSmallRoundButton from "../../components/AppSmallRoundButton.vue";

export default {
  name: "ConfigFactor",
  components: { AppSmallRoundButton, FactorConfigModal },
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
      dialog: false,
      loaded: false,
      factors: [],
      factor_value: null,
      dialog_input: { factor_value: null, factor_rules: [] },
    };
  },
  async mounted() {
    this.loaded = false;
    const res_factors = await axios.get(
      `/qry-config/factors?provision_id=${this.provision_id}`
    );
    this.factors = [...res_factors.data].sort((a, b) => {
      return a.factor_priority < b.factor_priority ? -1 : 1;
    });
    this.loaded = true;
  },
  computed: {
    output() {
      return this.factors.map((factor, index) => {
        return {
          ...factor,
          factor_priority: index,
          provision_id: this.provision_id,
        };
      });
    },
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: {
          product_id: this.product_id,
          provision_id: this.provision_id,
        },
        query: { ...params },
      });
    },
    updateRuleArray(payload) {
      const { factor_value, factor_rules, factor_priority } = payload;
      const factors = [...this.factors];
      let new_factor = {};
      if (factor_priority < this.factors.length) {
        new_factor = { ...this.factors[factor_priority] };
      }
      new_factor = { ...new_factor, factor_value, factor_rules };
      factors.splice(factor_priority, 1, { ...new_factor });
      this.factors = [...factors];
      this.dialog = false;
    },
    ruleDisplayHandler(rule) {
      const operators = { ...OPERATORS };
      return `${rule.field_name} ${operators[rule.comparison_operator_code]} ${
        rule.field_value
      }`;
    },
    moveRule(index, relative_positions) {
      const position = index + relative_positions;
      if (position >= 0 && position < this.factors.length) {
        const factors = [...this.factors];
        factors.splice(index, 1);
        factors.splice(position, 0, this.factors[index]);
        this.factors = [...factors];
      }
    },
    async deleteFactor(index) {
      const factor = this.factors[index];
      if (factor.factor_id) {
        try {
          await axios.delete(`/config/factor/${factor.factor_id}`);
          this.factors = this.factors.filter((value, ix) => {
            return ix !== index;
          });
        } catch (err) {
          console.log(err);
        }
      } else {
        this.factors = this.factors.filter((value, ix) => {
          return ix !== index;
        });
      }
    },
    editRules(ix = 99999999) {
      if (ix < this.factors.length) {
        this.dialog_input = {
          factor_priority: ix,
          factor_rules: [...this.factors[ix].factor_rules],
          factor_value: this.factors[ix].factor_value,
        };
      } else {
        this.dialog_input = {
          factor_priority: this.factors.length,
          factor_rules: [{}],
          factor_value: null,
        };
      }
      this.dialog = true;
    },
    async save() {
      await axios.post("/config/factor", this.output);
      this.routeTo("config-provision", { provision_id: this.provision_id });
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
