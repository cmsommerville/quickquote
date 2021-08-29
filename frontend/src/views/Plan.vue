<template>
  <div class="container">
    <div class="content" v-if="loaded">
      <b-form class="form" @submit="onSubmit" @reset="onReset" v-if="show">
        <div class="form-item">
          <div
            class="tile-wrapper"
            v-for="product in data.products"
            :key="product.name"
          >
            <input
              type="radio"
              :id="product.name"
              :value="product.name"
              v-model="selections.product_name"
            />
            <label :for="product.name">{{ product.text }}</label>
          </div>
        </div>

        <b-form-group
          class="form-item"
          label="Rating State:"
          label-for="input-state"
        >
          <b-form-select
            id="input-state"
            v-model="selections.rating_state"
            :options="states"
          ></b-form-select>
        </b-form-group>

        <b-form-group
          class="form-item"
          label="Effective Date:"
          label-for="input-tax-id"
        >
          <b-form-input
            id="input-tax-id"
            v-model="selections.plan_effective_date"
            type="date"
          ></b-form-input>
        </b-form-group>
        <div class="form-item buttons">
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  name: "Plan",
  data() {
    return {
      loaded: false,
      data: null,
      selections: {
        product_name: null,
        rating_state: null,
        plan_effective_date: null,
      },
      show: true,
    };
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/workflow/plan");
    this.data = { ...res.data };
    this.loaded = true;
  },
  computed: {
    states() {
      if (this.selections.product_name) {
        const product = this.data.products.find(
          (product) => product.name === this.selections.product_name
        );
        return product.statesApproved.map((stateObj) => {
          return {
            value: stateObj.state,
            text: stateObj.state,
          };
        });
      }
      return null;
    },
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      await axios.post("http://localhost:5000/workflow/plan", this.selections, {
        withCredentials: true,
      });

      // this.$router.push({ name: "ProductFactors" });
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.selections.product_name = null;
      this.selections.plan_effective_date = null;
      this.selections.rating_state = null;
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
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
  width: 60%;
  border: 1px solid #ddd;
  padding: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.form-item {
  margin: 0.5rem;
}

.tile-wrapper {
  width: 200px;
  height: 200px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: rgb(243, 222, 249);
  cursor: pointer;
  position: relative;

  display: flex;
  justify-content: center;
  align-items: center;
}

.tile-wrapper input {
  cursor: pointer;
  position: absolute;
  height: 100%;
  width: 100%;
  opacity: 0;
}

.tile-wrapper label {
  font-size: 2.2rem;
}
</style>
