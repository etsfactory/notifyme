<template>
  <sorteable-table :columns="columns" :data="users" class="users-table">
    <template slot="row" slot-scope="user">
      <td>{{ user.row.id }}</td>
      <td>{{ user.row.email }}</td>
      <td v-if="user.row.name">{{ user.row.name }}</td>
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
      { text: "Email", key: "email", sorteable: true }
    ]
  }),
  created() {
    if ("name" in this.users[0]) {
      this.addColumn("Name", "name", true);
    }
    this.addColumn("Actions", "actions", false, "actions");
  },
  methods: {
    navigateToUser(user_id) {
      this.$router.push({ name: "user", params: { id: user_id } });
    },
    addColumn(text, key, sorteable, className) {
      this.columns.push({
        text: text,
        key: key,
        sorteable: sorteable,
        class: className
      });
    },
    deleteUser(user_id) {
      this.$emit("deleted", user_id);
    }
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
