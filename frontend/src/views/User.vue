<template>
  <div class="user">
    <div v-if="user">
      <h1>User {{ $route.params.id }}</h1>
      <div>Email: {{user.email}}</div>
      <div v-if="notifications">
        <h2>Suscribed to:</h2>
        <sorteable-table :columns="columns" :data="notifications" class="notifications-table">
          <template slot="row" slot-scope="notification">
            <td>{{notification.row.exchange}}</td>
            <td>{{notification.row.exchange_type}}</td>
            <td v-if="notification.row.category">{{notification.row.category}}</td>
            <td v-if="notification.row.description">{{notification.row.description}}</td>
            <td class="actions">
              <i class="far fa-eye icon"></i>
              <i class="far fa-trash-alt icon"></i>
            </td>
          </template>
        </sorteable-table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import SorteableTable from "@/components/SorteableTable.vue";

export default {
  name: "User",
  components: {
    SorteableTable
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
        this.addColumn("Actions", "actions", false);
      });
    },
    addColumn(text, key, sorteable) {
      console.log(text);
      this.columns.push({ text: text, key: key, sorteable: sorteable });
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
