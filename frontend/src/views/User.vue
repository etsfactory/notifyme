<template>
  <div class="user">
    <div v-if="user">
      <h1>User {{nameToDisplay}}</h1>
      <div>Email: {{user.email}}</div>
      <div v-if="notifications">
        <h2>Suscribed to:</h2>
        <bus-filters-table :bus-filters="notifications"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import BusFiltersTable from "@/components/BusFiltersTable.vue";

export default {
  name: "User",
  components: {
    BusFiltersTable
  },
  data: () => ({
    user: null,
    notifications: null,
    usersApi: "/users/",
    notificationsApi: "/bus_filters",
    columns: [
      { text: "Exchange", key: "exchange", sorteable: true },
      { text: "Exchange Type", key: "exchange_type", sorteable: false }
    ]
  }),
  computed: {
    nameToDisplay() {
      if ("name" in this.user ) { return this.user.name }
      return this.user.id
    }
  },
  methods: {
    getUser(id) {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST + this.usersApi + id;
      axios.get(usersEndpoint).then(response => {
        this.user = response.data;
        this.getUserNotifications(this.$route.params.id);
      });
    },
    getUserNotifications(id) {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.usersApi +
        id +
        this.notificationsApi;
      axios.get(usersEndpoint).then(response => {
        this.notifications = response.data;
        if ("description" in this.notifications[0]) {
          this.addColumn("Description", "description", true);
        }
        if ("category" in this.notifications[0]) {
          this.addColumn("Category", "category", true);
        }
        this.addColumn("Actions", "actions", false, "actions" );
      });
    },
    addColumn(text, key, sorteable, class_name) {
      this.columns.push({ text: text, key: key, sorteable: sorteable, class: class_name });
    }
  },
  created() {
    this.getUser(this.$route.params.id);
  }
};
</script>

<style lang="scss" scoped>
.notifications-table /deep/.actions {
  text-align: center !important;
}
.icon {
  padding: 0 3rem;
  cursor: pointer;
  &:hover {
    color: $color-main-dark;
  }
}
</style>
