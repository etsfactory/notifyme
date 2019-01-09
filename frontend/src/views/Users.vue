<template>
  <div class="users">
    <h1>Users</h1>
    <sorteable-table :columns="columns" :data="users"></sorteable-table>
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
        { text: "id", name: "id", sorteable: true },
        { text: "email", name: "email", sorteable: true }
      ];
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
</style>
