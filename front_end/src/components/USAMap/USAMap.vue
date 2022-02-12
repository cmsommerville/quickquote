<template>
  <div class="relative">
    <div
      id="tooltip"
      v-if="tooltip_data"
      :style="{ top: tooltip_Y + 'px', left: tooltip_X + 'px' }"
    >
      <h3 class="text-sm mb-1 pa-2">State: {{ tooltip_data.state_code }}</h3>
      <p
        v-if="
          tooltip_data.state_effective_date &&
          tooltip_data.state_expiration_date
        "
        class="text-xs"
      >
        {{ formatDateText(tooltip_data.state_effective_date) }}
        thru
        {{ formatDateText(tooltip_data.state_expiration_date) }}
      </p>
      <p v-else class="text-xs">Not configured yet!</p>
    </div>
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
      viewBox="170 90 960 600"
      enable-background="new 0 0 959 593"
      xml:space="preserve"
    >
      <defs>
        <pattern
          id="disabled"
          width="8"
          height="10"
          patternUnits="userSpaceOnUse"
          patternTransform="rotate(45 50 50)"
        >
          <line stroke="#d1d5db" stroke-width="7px" y2="10" />
        </pattern>
      </defs>
      <g id="g5">
        <path
          v-for="state in states"
          :key="state.state_code"
          :id="state.state_code"
          :fill="fillColor(state)"
          :d="state.svg_path"
          @click="select(state)"
          @mouseleave="tooltip_data = null"
          @mouseover="hover(state)"
          @mousemove="displayTooltip"
        />
        <g id="gDC" v-for="dist in DC" :key="dist.state_code">
          <path id="pathDC" :fill="dist.fill" :d="dist.svg_path" />
          <circle
            id="circleDC"
            :fill="fillColor(dist)"
            :stroke="dist.stroke"
            :stroke-width="dist['stroke-width']"
            :cx="dist.cx"
            :cy="dist.cy"
            :r="dist.r"
            @click="select(dist)"
            @mouseleave="tooltip_data = null"
            @mouseover="hover(dist)"
            @mousemove="displayTooltip"
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
import { format } from "date-fns";
import axios from "@/services/axios.js";

export default {
  name: "UnitedStatesMap",
  props: {
    configured_states: {
      default: [],
      type: Array,
    },
    fill_default: {
      default: "var(--gray-300)",
      type: String,
    },
    fill_disabled: {
      default: "var(--gray-100)",
      type: String,
    },
    fill_selected: {
      default: "var(--theme-500)",
      type: String,
    },
  },
  async mounted() {
    const ref_states = await axios.get("/config/ref-states");
    const all_states = [
      ...ref_states.data
        .filter((st) => !!st.svg_path)
        .map((item) => {
          const config_states =
            this.configured_states.find(
              (cs) => cs.state_code === item.state_code
            ) ?? {};
          if (config_states.state_code) {
            config_states.fill = this.fill_disabled;
            config_states.disabled = true;
          } else {
            config_states.fill = this.fill_default;
          }
          return {
            ...item,
            ...config_states,
          };
        }),
    ];

    this.$store.commit("initialize_ref_states", all_states);
    this.$store.commit("initialize_selected_states", []);
  },
  data() {
    return {
      tooltip_data: null,
      tooltip_X: null,
      tooltip_Y: null,
    };
  },
  computed: {
    all_states() {
      return this.$store.getters.get_ref_states;
    },
    selected_states() {
      return this.$store.getters.get_selected_states;
    },
    states() {
      return this.all_states.filter((state) => state.state_code !== "DC");
    },
    DC() {
      const dc = this.all_states
        .filter((state) => state.state_code === "DC")
        .map((st) => {
          return {
            stroke: "#FFFFFF",
            "stroke-width": "1.5",
            cx: "975.3",
            cy: "351.8",
            r: "7",
            ...st,
          };
        });
      return dc;
    },
  },
  methods: {
    displayTooltip(ev) {
      this.tooltip_Y = ev.offsetY;
      this.tooltip_X = ev.offsetX + 30;
    },
    hover(state) {
      this.tooltip_data = state;
    },
    select(state) {
      if (!state.disabled) this.$store.commit("toggle_selected_state", state);
    },
    fillColor(state) {
      if (state.disabled) return "url(#disabled)";
      if (
        this.selected_states.findIndex(
          (st) => st.state_code === state.state_code
        ) >= 0
      )
        return this.fill_selected;
      return state.fill;
    },
    formatDateText(input_dt) {
      const dt = new Date(input_dt);
      const dtDateOnly = new Date(
        dt.valueOf() + dt.getTimezoneOffset() * 60 * 1000
      );
      return format(dtDateOnly, "M/d/yyyy");
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

#tooltip {
  position: absolute;
  top: 0px;
  left: 0px;
  z-index: 1;
  background-color: #fff;
  border: 2px solid var(--theme-400);
  border-radius: 5px;
  padding: 5px;
  overflow: hidden;
}

path:hover,
circle:hover {
  stroke: var(--theme-600);
  stroke-width: 2px;
  stroke-linejoin: round;
  fill: var(--theme-600);
  cursor: pointer;
}
#path67 {
  fill: none !important;
  stroke: #a9a9a9 !important;
  cursor: default;
}

.stripe {
  color: white;
  background: repeating-linear-gradient(
    45deg,
    var(--gray-100),
    var(--gray-100) 10px,
    var(--gray-200) 10px,
    var(--gray-200) 20px
  );
}
</style>
