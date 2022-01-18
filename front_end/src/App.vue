<template>
  <div
    class="
      min-w-screen min-h-screen
      bg-gradient-to-br
      from-red-500
      to-orange-500
      bg-cover
    "
  >
    <header>
      <the-header />
    </header>
    <main class="h-full flex justify-center text-gray-600">
      <div class="w-4/6 my-6">
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
