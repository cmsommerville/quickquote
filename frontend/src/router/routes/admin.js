import CreateTables from "../../views/admin/CreateTables.vue";
import Session from "../../views/admin/Session.vue";
import InsertRateTables from "../../views/admin/InsertRateTables.vue";

export default [
  {
    path: "/admin/create-tables",
    name: "create-tables",
    component: CreateTables,
  },
  {
    path: "/admin/insert-rate-tables",
    name: "admin-rate-tables",
    component: InsertRateTables,
  },
  {
    path: "/session",
    name: "session",
    component: Session,
  },
];
