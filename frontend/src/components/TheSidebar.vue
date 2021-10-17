<template>
  <v-navigation-drawer app temporary :value="drawer" @input="inputHandler">
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="text-h6">
          <the-logo />
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>
    <v-list dense nav>
      <v-list-item-group color="accent">
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
          exact
          :to="{ name: item.to }"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import TheLogo from "./TheLogo.vue";

export default {
  name: "TheSidebar",
  components: { TheLogo },
  props: {
    drawer: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      items: [
        { title: "Home", icon: "mdi-view-dashboard", to: "Home" },
        { title: "New Quote", icon: "mdi-text-box-plus", to: "rater" },
        {
          title: "Create Tables",
          icon: "mdi-table-large",
          to: "create-tables",
        },
        {
          title: "Insert Rates",
          icon: "mdi-currency-usd",
          to: "admin-rate-tables",
        },
        {
          title: "View Session",
          icon: "mdi-account-cog",
          to: "session",
        },
      ],
      right: null,
    };
  },
  methods: {
    inputHandler(payload) {
      this.$emit("toggle", payload);
    },
  },
};
</script>

<style scoped></style>
