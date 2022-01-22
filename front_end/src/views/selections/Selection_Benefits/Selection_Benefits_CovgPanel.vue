<template>
  <div class="rounded-md shadow-md">
    <div
      :class="{
        'px-12': true,
        'py-4': true,
        flex: true,
        'justify-between': true,
        'items-center': true,
        'mb-6': true,
        'bg-gray-50': true,
        'border-b-2': !hidden,
        'border-b-gray-200': !hidden,
        'rounded-t-md': true,
      }"
    >
      <h2 class="text-lg">{{ coverage.coverage_label }}</h2>
      <app-button
        class="border-0"
        :fab="true"
        :transparent="true"
        @click="hidden = !hidden"
      >
        <arrow-circle-down-icon
          v-if="hidden"
          class="h-8 w-8 text-theme-primary"
        />
        <arrow-circle-up-icon
          v-if="!hidden"
          class="h-8 w-8 text-theme-primary"
        />
      </app-button>
    </div>
    <transition name="slide-fade" mode="out-in">
      <div class="px-12 pb-12" v-if="!hidden">
        <div class="grid grid-cols-2 gap-4">
          <app-input
            v-for="benefit in benefits"
            :key="benefit.benefit_id"
            class="w-24"
            :prefix="benefit.unit_code === 'Dollar' ? '$' : ''"
            :suffix="benefit.unit_code === 'Percent' ? '%' : ''"
            v-model.number="benefit.ui_benefit_value"
            @input="emitValues"
            >{{ benefit.benefit_label }}</app-input
          >
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ArrowCircleDownIcon, ArrowCircleUpIcon } from "@heroicons/vue/outline";

export default {
  name: "Selection_Benefits_CovgPanel",
  components: { ArrowCircleDownIcon, ArrowCircleUpIcon },
  props: {
    coverage: {
      type: Object,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      hidden: true,
      selected: false,
      benefits: [],
    };
  },
  mounted() {
    this.selected = this.coverage.default_value;
    this.benefits = this.coverage.benefits;
    this.emitValues();
  },
  methods: {
    toggleCoverage() {
      this.benefits.map((bnft) => {
        bnft.ui_selection_value = this.selected
          ? (bnft.selected_benefit && bnft.selected_benefit.benefit_value) ??
            bnft.default_value
          : 0;
        if (bnft.durations) {
          for (const dur of bnft.durations) {
            const default_val = dur.duration_items.find((item) => {
              return item.item_code === dur.default_duration_item_code;
            });
            dur.ui_selection_value = this.selected
              ? default_val ?? dur.duration_items[0]
              : null;
          }
        }
      });
      this.emitValues();
    },
    emitValues() {
      this.$emit("selections:change", {
        coverage_code: this.coverage.coverage_code,
        benefits: this.benefits,
      });
    },
  },
};
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.2s;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>
