<template>
  <sorteable-table :columns="columns" :data="users" class="users-table">
    <template slot="row" slot-scope="user">
      <td>{{ user.row.id }}</td>
      <td>{{ user.row.email }}</td>
      <td>{{ user.row.name }}</td>
      <td class="actions">
        <i class="far fa-eye icon" @click="navigateToUser(user.row.id)"></i>
        <i class="far fa-trash-alt icon" @click="deleteUser(user.row.id)"></i>
      </td>
    </template>
  </sorteable-table>
</template>

<script>
import SorteableTable from "@/components/SorteableTable.vue";

export default {
  name: "UsersTable",
  components: {
    SorteableTable
  },
  props: {
    users: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    columns: [
      { text: "Id", key: "id", sorteable: true },
      { text: "Email", key: "email", sorteable: true },
      { text: "Name", key: "name", sorteable: true },
      { text: "", key: "actions", sorteable: false }
    ]
  }),
  methods: {
    navigateToUser(user_id) {
      this.$router.push({ name: "user", params: { id: user_id } });
    },
    deleteUser(user_id) {
      this.$emit("deleted", user_id);
    }
  }
};
</script>

<style lang="scss" scoped>

</style>
