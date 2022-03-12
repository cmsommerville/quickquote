<template>
  <div
    class="absolute -bottom-8 -right-6 flex flex-col"
    @mouseenter="show_fab = true"
    @mouseleave="show_fab = false"
  >
    <transition name="scale-up">
      <div v-if="show_fab">
        <app-modal
          :fab="true"
          :disabled="disabled_delete"
          class="bg-red-700 text-white mb-4 border-2 border-red-700 disabled:border-gray-200"
          ><x-icon class="h-16 w-16 p-5" />
          <template #header>Are you sure?</template>
          <template #content="contentProps">
            <div class="flex justify-center items-center mx-32 my-8">
              <app-button
                class="bg-red-700 mr-8"
                @click="_deleteHandler(contentProps.close)"
                >Delete record</app-button
              >
              <app-button :transparent="true" @click="contentProps.close"
                >Cancel</app-button
              >
            </div>
          </template>
        </app-modal>
      </div>
    </transition>
    <transition name="scale-up">
      <div v-if="show_fab">
        <app-button
          class="bg-white text-theme-primary border-2 border-theme-primary mb-4 disabled:border-gray-200"
          :disabled="disabled_edit"
          :fab="true"
          @click="$emit('fab:edit')"
          ><pencil-icon class="h-16 w-16 p-5"
        /></app-button>
      </div>
    </transition>

    <app-button
      class="mr-8 border-2 border-theme-primary disabled:border-gray-200"
      :disabled="disabled_new"
      :fab="true"
      @click="$emit('fab:new')"
      ><plus-icon class="h-16 w-16 p-5"
    /></app-button>
  </div>
</template>

<script>
import AppModal from "@/components/AppModal.vue";

export default {
  name: "AppNewEditDeleteButton",
  components: { AppModal },
  emits: ["fab:new", "fab:edit", "fab:delete"],
  props: {
    disabled_new: {
      default: false,
    },
    disabled_edit: {
      default: false,
    },
    disabled_delete: {
      default: false,
    },
  },
  data() {
    return {
      show_fab: false,
    };
  },
  methods: {
    _deleteHandler(callback) {
      this.$emit("fab:delete");
      callback();
    },
  },
};
</script>

<style scoped lang="scss">
.scale-up-enter-active,
.scale-up-leave-active {
  transition: all 0.3s ease;
}

.scale-up-enter-from,
.scale-up-leave-to {
  transform: translateY(2rem);
  opacity: 0;
}
</style>
