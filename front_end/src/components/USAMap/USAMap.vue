<template>
  <div class="">
    <svg
      xmlns:cc="http://creativecommons.org/ns#"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
      xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
      xmlns:svg="http://www.w3.org/2000/svg"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      version="1.1"
      id="us-map"
      preserveAspectRatio="xMinYMin meet"
      inkscape:version="0.91 r13725"
      x="0px"
      y="0px"
      viewBox="174 100 959 593"
      enable-background="new 174 100 959 593"
      xml:space="preserve"
    >
      <g id="g5">
        <path
          v-for="state in states"
          :key="state.id"
          :id="state.id"
          :fill="
            selected_states.includes(state.id) ? fill_selected : state.fill
          "
          :d="state.d"
          @click="select(state.id)"
        />
        <g id="gDC" v-for="dist in DC" :key="dist.id">
          <path id="pathDC" :fill="dist.fill" :d="dist.d" />
          <circle
            id="circleDC"
            :fill="
              selected_states.includes(dist.id) ? fill_selected : dist.fill
            "
            :stroke="dist.stroke"
            :stroke-width="dist['stroke-width']"
            :cx="dist.cx"
            :cy="dist.cy"
            :r="dist.r"
            @click="select(dist.id)"
          />
        </g>
      </g>
      <path
        id="path67"
        fill="none"
        stroke="#A9A9A9"
        stroke-width="2"
        d="M385,593v55l36,45 M174,525h144l67,68h86l53,54v46"
      />
    </svg>
  </div>
</template>

<script>
import { states } from "./states.js";

export default {
  name: "UnitedStatesMap",
  props: {
    product_states: {
      required: true,
      type: Array,
    },
    fill_default: {
      default: "var(--gray-300)",
      type: String,
    },
    fill_selected: {
      default: "var(--violet-500)",
      type: String,
    },
    fill_active: {
      default: "var(--violet-300)",
      type: String,
    },
  },
  mounted() {
    this._states = states.map((state) => {
      const ps =
        this.product_states.find((ps) => ps.state_code === state.id) ?? {};

      if (ps.state_code) {
        ps.fill = this.fill_active;
      } else {
        ps.fill = this.fill_default;
      }
      return {
        ...state,
        ...ps,
      };
    });
  },
  data() {
    return {
      _states: [],
      selected_states: [],
    };
  },
  computed: {
    states() {
      return this._states.filter((state) => state.id !== "DC");
    },
    DC() {
      const dc = this._states.filter((state) => state.id === "DC");
      return dc;
    },
  },
  methods: {
    select(_id) {
      if (this.selected_states.includes(_id)) {
        this.selected_states = this.selected_states.filter((st) => st !== _id);
      } else {
        this.selected_states.push(_id);
      }
      this.$emit("select:state", this.selected_states);
    },
  },
};
</script>

<style scoped>
#us-map {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
path:hover,
circle:hover {
  stroke: var(--violet-600);
  stroke-width: 2px;
  stroke-linejoin: round;
  fill: var(--violet-600);
  cursor: pointer;
}
#path67 {
  fill: none !important;
  stroke: #a9a9a9 !important;
  cursor: default;
}
</style>
