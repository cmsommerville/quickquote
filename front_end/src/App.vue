<template>
  <div class="min-w-screen min-h-screen bg-slate-100">
    <header>
      <the-header />
    </header>
    <main class="h-full flex justify-center text-gray-600">
      <div class="sm:w-5/6 2xl:w-2/3 my-6">
        <router-view v-slot="{ Component }" :key="$route.fullPath">
          <transition name="slide-fade" mode="out-in">
            <component :is="Component"></component>
          </transition>
        </router-view>
      </div>
    </main>
    <app-snackbar />
  </div>
</template>

<script>
import TheHeader from "./components/TheHeader.vue";
import AppSnackbar from "@/components/AppSnackbar.vue";

export default {
  name: "App",
  components: { TheHeader, AppSnackbar },
};
</script>

<style lang="scss">
@import "ag-grid-community/dist/styles/ag-grid.css";
@import "ag-grid-community/dist/styles/ag-theme-alpine.css";

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
