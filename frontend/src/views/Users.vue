<template>
  <div class="users">
    <h1>Users</h1>
    <users-table v-if="users" :users="users"/>
  </div>
</template>

<script>
import axios from "axios";
import UsersTable from "@/components/UsersTable.vue";

export default {
  name: "Users",
  components: {
    UsersTable
  },
  data: () => ({
    usersApi: "/users",
    users: null
  }),
  created() {
    const usersEndpoint = process.env.VUE_APP_NOTIFYME_HOST + this.usersApi;
    axios.get(usersEndpoint).then(response => {
      this.users = response.data;
    });
  }
};
</script>

<style lang="scss" scoped>

</style>
