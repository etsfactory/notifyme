<template>
  <div class="users">
    <h1>
      <i class="fas fa-users"></i> Users
      <i class="fas fa-plus-circle create-icon" @click="createUser"></i>
    </h1>
    <users-table v-if="users" :users="users" @deleted="showModal"/>
    <confirm-modal :visible.sync="showDeleteModal" @accept="deleteUser"/>
    <create-user :visible.sync="showCreateModal" @created="getUsers"/>
  </div>
</template>

<script>
import usersApi from "@/logic/users";

import UsersTable from "@/components/UsersTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateUser from "@/components/CreateUser.vue";

export default {
  name: "Users",
  components: {
    UsersTable,
    ConfirmModal,
    CreateUser
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
      let response = await usersApi.getAll();
      this.users = response.data;
    },
    showModal(user_id) {
      this.showDeleteModal = true;
      this.selectedUser = user_id;
    },
    async deleteUser() {
      this.closeModal();
      await usersApi.delete(this.selectedUser);
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
