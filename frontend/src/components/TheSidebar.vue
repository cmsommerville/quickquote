<template>
  <v-navigation-drawer permanent app clipped>
    <v-list dense nav>
      <v-list-item-group color="primary">
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
export default {
  name: "TheSidebar",
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
};
</script>

<style scoped></style>
