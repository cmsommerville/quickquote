<template>
  <div v-if="loaded">
    <v-card
      class="mx-auto mt-6"
      width="80%"
      tile
      v-for="bnft in plan_config.benefits"
      :key="bnft.name"
    >
      <v-list-item>
        <v-list-item-content>
          <v-row>
            <v-col
              class="d-flex justify-center"
              cols="12"
              xs="12"
              sm="8"
              lg="9"
            >
              <v-list-item-title>{{ bnft.text }}</v-list-item-title>
            </v-col>
            <v-col cols="12" xs="12" sm="4" lg="3">
              <component
                :is="bnft.ui.component"
                v-bind="{ ...bnft.ui }"
                :name="bnft.name"
                v-model="selections[bnft.name]"
              />
            </v-col>
          </v-row>
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </div>
</template>

<script>
import axios from "../services/axios.js";
import { VTextField, VSelect, VSwitch } from "vuetify/lib";

export default {
  name: "Benefits",
  components: {
    VSelect,
    VTextField,
    VSwitch,
  },
  data() {
    return {
      loaded: false,
      plan_config_id: null,
      plan_config: null,
      selections: {},
    };
  },
  async mounted() {
    this.plan_config_id = "615ba44644247be1d00ab650";

    const res = await axios.get(`/config/plan/${this.plan_config_id}`);
    this.plan_config = { ...res.data[0] };

    this.selections = [...res.data[0].benefits].reduce(
      (acc, curr) => (
        (acc[curr.name] = curr.amounts.default ? curr.amounts.default : null),
        acc
      ),
      {}
    );
    this.loaded = true;
  },
};
</script>

<style></style>
