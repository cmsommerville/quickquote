<template>
  <div>
    <div class="content" v-if="loaded && benefit_durations.length === 0">
      <v-card class="d-flex justify-space-between">
        <div class="card-content">
          <v-card-title>Setup a duration!</v-card-title>
          <v-card-subtitle
            >No benefit durations configured yet!</v-card-subtitle
          >
        </div>
        <v-fab-transition>
          <v-btn
            color="pink"
            dark
            absolute
            bottom
            fab
            right
            @click="routeTo('config-benefit-duration')"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-fab-transition>
      </v-card>
    </div>
    <div class="content" v-if="loaded && benefit_durations.length > 0">
      <v-row v-for="dur in benefit_durations" :key="dur.benefit_duration_id">
        <v-col cols="12" xs="12">
          <v-card class="d-flex justify-space-between">
            <div class="card-content">
              <v-card-title>{{ dur.duration.duration_label }}</v-card-title>
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
                    @click="edit(dur.benefit_duration_id)"
                    ><v-icon color="primary">mdi-pencil</v-icon></v-btn
                  >
                </template>
                <span>Edit Benefit Duration</span>
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
          @click="routeTo('config-benefit')"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-fab-transition>
    </div>
    <v-divider></v-divider>
    <div class="call-to-action d-flex justify-center align-center mt-4">
      <v-btn color="primary" class="mx-4" @click="routeTo('config-benefit')">
        Back to Benefit
      </v-btn>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigBenefitDurations",
  props: {
    product_id: {
      required: true,
      type: Number,
    },
    benefit_id: {
      required: true,
      type: Number,
    },
  },
  data() {
    return {
      loaded: false,
      benefit_durations: [],
    };
  },
  async mounted() {
    this.loaded = false;
    const res = await axios.get(
      `/qry-config/all-benefit-durations?benefit_id=${this.benefit_id}`
    );
    this.benefit_durations = [...res.data];
    this.loaded = true;
  },
  methods: {
    routeTo(route_name, params = {}) {
      this.$router.push({
        name: route_name,
        params: { benefit_id: this.benefit_id, product_id: this.product_id },
        query: { ...params },
      });
    },
    edit(id) {
      this.routeTo("config-benefit-duration", { benefit_duration_id: id });
    },
  },
};
</script>

<style scoped></style>
