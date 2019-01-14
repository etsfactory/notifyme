<template>
  <div class="user">
    <div v-if="busFilter">
      <h1><i class="fas fa-filter"></i> BusFilter</h1>
      <key-value-table class="info" :data="busFilter"/>
      <div v-if="notifications" class="users">
        <h2><i class="fas fa-users"></i> Users suscribed to:</h2>
        <users-table :users="notifications"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UsersTable from "@/components/UsersTable.vue";
import KeyValueTable from "@/components/KeyValueTable.vue";

export default {
  name: "BusFilter",
  components: {
    UsersTable,
    KeyValueTable
  },
  data: () => ({
    busFilter: null,
    notifications: null,
    usersApi: "/users",
    busFiltersApi: "/bus_filters/"
  }),
  created() {
    this.getBusFilter(this.$route.params.id);
  },
  methods: {
    getBusFilter(id) {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST + this.busFiltersApi + id;
      axios.get(usersEndpoint).then(response => {
        this.busFilter = response.data;
        this.getUserNotifications(this.$route.params.id);
      });
    },
    getUserNotifications(id) {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.busFiltersApi +
        id +
        this.usersApi;
      axios.get(usersEndpoint).then(response => {
        this.notifications = response.data;
      });
    }
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
.info {
  width: 40%;
}
.users {
  margin-top: 3rem;
}
</style>
