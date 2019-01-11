<template>
  <div class="users">
    <h1>
      <i class="fas fa-users"></i> Users
    </h1>
    <users-table v-if="users" :users="users" @deleted="showModal"/>
    <confirm-modal :visible.sync="openModal" @close="closeModal" @accept="deleteUser"/>
  </div>
</template>

<script>
import axios from "axios";
import UsersTable from "@/components/UsersTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";

export default {
  name: "Users",
  components: {
    UsersTable,
    ConfirmModal
  },
  data: () => ({
    usersApi: "/users",
    users: null,
    openModal: false,
    selectedUser: null
  }),
  methods: {
    getUsers() {
      const usersEndpoint = process.env.VUE_APP_NOTIFYME_HOST + this.usersApi;
      axios.get(usersEndpoint).then(response => {
        this.users = response.data;
      });
    },
    showModal(user_id) {
      this.openModal = true;
      this.selectedUser = user_id;
    },
    closeModal() {
      this.openModal = false;
    },
    deleteUser() {
      this.openModal = false;
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.usersApi +
        "/" +
        this.selectedUser;
      axios.delete(usersEndpoint).then(() => {
        this.getUsers();
      });
    }
  },
  created() {
    this.getUsers();
  }
};
</script>

<style lang="scss" scoped>
</style>
