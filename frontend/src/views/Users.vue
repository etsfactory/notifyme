<template>
  <div class="users">
    <h1>Users</h1>
    <sorteable-table :columns="columns" :data="users" class="users-table">
      <template slot="row" slot-scope="user">
        <td>
          {{ user.row.id }}
        </td>
        <td>
          {{ user.row.email }}
        </td>
        <td class="actions">
          <i class="far fa-eye icon" @click="navigateToUser(user.row.id)"></i>
          <i class="far fa-trash-alt icon"></i>
        </td>
      </template>
    </sorteable-table>
  </div>
</template>

<script>
import axios from "axios";
import SorteableTable from "@/components/SorteableTable.vue";

export default {
  name: "Users",
  components: {
    SorteableTable
  },
  data: () => ({
    usersApi: "/users",
    users: null,
  }),
  computed: {
    columns() {
      return [
        { text: "Id", key: "id", sorteable: true },
        { text: "Email", key: "email", sorteable: true },
        { text: "Actions", key: "actions", sorteable: false , class: "actions" }
      ];
    }
  },
  methods: {
    navigateToUser(user_id) {
      this.$router.push({ name: 'user', params: { id: user_id }});
    }
  },
  created() {
    const usersEndpoint = process.env.VUE_APP_NOTIFYME_HOST + this.usersApi;
    axios.get(usersEndpoint).then(response => {
      this.users = response.data;
    });
  }
};
</script>

<style lang="scss" scoped>
.users-table /deep/.actions {
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
