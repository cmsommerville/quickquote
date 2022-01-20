<template>
  <div class="min-w-screen min-h-screen bg-slate-100">
    <header>
      <the-header />
    </header>
    <main class="h-full flex justify-center text-gray-600">
      <div class="min-w-4/6 my-6">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script>
import TheHeader from "./components/TheHeader.vue";
export default {
  name: "App",
  components: { TheHeader },
};
</script>
