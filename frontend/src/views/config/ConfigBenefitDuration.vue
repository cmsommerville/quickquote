<template>
  <div>
    <div>
      <v-form class="d-flex justify-space-around">
        <v-text-field
          class="mx-12 my-3"
          v-model="benefit_duration.duration.duration_label"
          filled
          outlined
          label="Benefit Duration Name"
        />

        <v-text-field
          class="mx-12 my-3"
          v-model="benefit_duration.benefit_duration_code"
          filled
          outlined
          label="Benefit Code"
        />
      </v-form>
    </div>

    <div>
      <div class="mt-6">
        <v-list-item v-for="item in duration_items" :key="item._id" dense>
          <v-text-field
            class="mx-6"
            v-model="item.item_code"
            filled
            outlined
            dense
            label="Duration Item Code"
          />
          <v-text-field
            class="mx-6"
            v-model="item.item_label"
            filled
            outlined
            dense
            label="Duration Item Label"
          />
          <v-text-field
            class="mx-6"
            v-model="item.benefit_duration_factor"
            filled
            outlined
            dense
            type="number"
            min="0"
            label="Duration Factor"
          />
          <v-checkbox
            v-model="duration_default_id"
            :success="item._id === duration_default_id"
            :value="item._id"
            label="Is Default"
          />
        </v-list-item>
      </div>
      <v-divider></v-divider>
      <div class="call-to-action d-flex justify-center align-center mt-4">
        <v-btn color="primary" class="mx-4" @click="save"> Save </v-btn>
        <v-btn color="secondary" class="mx-4" @click="addDurationItem">
          Add Item
        </v-btn>

        <v-btn color="primary" class="mx-4" @click="routeTo('config-benefit')">
          Back
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

export default {
  name: "ConfigBenefitDuration",
  props: {
    product_id: {
      required: true,
      type: [Number, String],
    },
    benefit_id: {
      required: true,
      type: [Number, String],
    },
  },
  async mounted() {
    this.loaded = false;

    if (this.$route.query.benefit_duration_id) {
      this.editable = false;
      const res = await axios.get(
        `/config/benefit-duration/${this.$route.query.benefit_duration_id}`
      );
      this.benefit_duration_id = this.$route.query.benefit_duration_id;
      this.initializeData(res.data);
    } else {
      this.initializeData();
    }

    this.loaded = true;
  },
  data() {
    return {
      loaded: false,
      editable: true,
      benefit_duration_id: null,
      benefit_duration: {
        benefit_id: null,
        benefit_duration_code: null,
        default_value: null,
        benefit: {},
        duration: {},
      },
      duration_items: [],
      duration_default_id: null,
    };
  },
  computed: {
    valid() {
      return true;
    },
    default_duration_item_code() {
      const def =
        this.duration_items.find(
          (item) => item._id === this.duration_default_id
        ) ?? this.duration_items[0];
      return def.item_code;
    },
    items() {
      return [
        ...this.duration_items
          .filter((item) => !!item.item_code)
          .map((i) => this.formatDurationItems(i)),
      ];
    },
    output() {
      const duration = {
        ...this.benefit_duration,
        default_duration_item_code: this.default_duration_item_code,
        duration: {
          duration_code: this.benefit_duration.benefit_duration_code,
          duration_label: this.benefit_duration.duration.duration_label,
        },
        benefit_id: this.benefit_id,
      };
      if (this.items.length > 0) {
        duration.duration_items = [...this.items];
      }
      return duration;
    },
  },
  methods: {
    formatDurationItems(i) {
      /* eslint-disable no-unused-vars */
      const { _id, item_label, ...item } = i;
      /* eslint-enable no-unused-vars */
      return {
        ...item,
        benefit_duration_id: this.benefit_duration_id,
        duration_item: {
          item_code: item.item_code,
          item_label: item_label,
        },
      };
    },
    initializeData(config = {}) {
      this.benefit_duration = {
        benefit_duration_code: null,
        duration: {
          duration_code: null,
          duration_label: null,
        },
        ...config,
      };

      if (config.duration_items) {
        this.duration_items = [
          ...config.duration_items.map((item) => {
            return {
              ...item,
              _id: Math.random(),
              item_label: item.duration_item.item_label,
            };
          }),
        ];
      }

      if (config.benefit_duration_id) {
        this.benefit_duration_id = config.benefit_duration_id;
      }
    },
    routeTo(name, params = {}) {
      this.$router.push({
        name: name,
        params: {
          product_id: this.product_id,
          benefit_id: this.benefit_id,
        },
        query: {
          ...params,
        },
      });
    },

    addDurationItem() {
      this.duration_items = [
        ...this.duration_items,
        {
          _id: Math.random(),
          item_code: null,
          benefit_duration_factor: null,
          item_label: null,
        },
      ];
    },
    async save() {
      let res;
      if (this.benefit_duration_id) {
        res = await axios.put(
          `/config/benefit-duration/${this.benefit_duration_id}`,
          {
            ...this.output,
            benefit_duration_id: this.benefit_duration_id,
          }
        );
      } else {
        res = await axios.post("/config/benefit-duration", {
          ...this.output,
        });
      }
      this.benefit_duration_id = res.data.benefit_duration_id;
    },
  },
};
</script>

<style scoped>
.main-section {
  display: grid;
  grid-template-columns: 3fr 2fr;
  column-gap: 30px;
  row-gap: 15px;
}

.config-cards {
  display: grid;
  grid-template-columns: 1fr;
  row-gap: 15px;
}

.btn-edit {
  position: absolute;
  top: -15px;
  right: -15px;
}
</style>
