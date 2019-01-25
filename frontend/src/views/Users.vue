<template>
  <div class="users">
    <h1>
      <i class="fas fa-users"></i> Users
      <i class="fas fa-plus-circle create-icon" @click="createUser"></i>
    </h1>
    <error v-if="error" :error="error"/>
    <users-table v-else-if="users" :users="users" @deleted="showModal"/>
    <confirm-modal :visible.sync="showDeleteModal" @accept="deleteUser"/>
    <create-user :visible.sync="showCreateModal" @created="getUsers"/>
  </div>
</template>

<script>
import usersApi from "@/logic/users";

import UsersTable from "@/components/UsersTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateUser from "@/components/CreateUser.vue";
import Error from "@/components/Error.vue";

export default {
  name: "Users",
  components: {
    UsersTable,
    ConfirmModal,
    CreateUser,
    Error
  },
  data: () => ({
    users: null,
    showDeleteModal: false,
    selectedUser: null,
    showCreateModal: false,
    error: null
  }),
  created() {
    this.getUsers();
  },
  methods: {
    async getUsers() {
      try {
        let response = await usersApi.getAll();
        this.users = response.data;
      } catch (error) {
        this.error = error.response;
      }
    },
    showModal(user_id) {
      this.showDeleteModal = true;
      this.selectedUser = user_id;
    },
    async deleteUser() {
      this.showDeleteModal = false;
      try {
        await usersApi.delete(this.selectedUser);
      } catch (error) {
        this.error = error.response;
      }
      this.getUsers();
    },
    createUser() {
      this.showCreateModal = true;
    }
  }
};
</script>

<style lang="scss" scoped>
.users {
  position: relative;
}
</style>
