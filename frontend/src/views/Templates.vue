<template>
  <div class="users">
    <h1>
      <i class="fas fa-envelope"></i> Templates
      <i class="fas fa-plus-circle create-icon" @click="createUser"></i>
    </h1>
    <template-table v-if="users" :templates="users" @deleted="showModal"/>
    <confirm-modal :visible.sync="showDeleteModal" @close="closeModal" @accept="deleteUser"/>
    <create-user :visible.sync="showCreateModal" @created="getUsers"/>
  </div>
</template>

<script>
import axios from "axios";
import TemplateTable from "@/components/TemplateTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateUser from "@/components/CreateUser.vue";

export default {
  name: "Templates",
  components: {
    TemplateTable,
    ConfirmModal,
    CreateUser
  },
  data: () => ({
    usersApi: "/templates",
    users: null,
    showDeleteModal: false,
    selectedUser: null,
    showCreateModal: false
  }),
  created() {
    this.getUsers();
  },
  methods: {
    getUsers() {
      const usersEndpoint = process.env.VUE_APP_NOTIFYME_HOST + this.usersApi;
      axios.get(usersEndpoint).then(response => {
        this.users = response.data;
      });
    },
    showModal(user_id) {
      this.showDeleteModal = true;
      this.selectedUser = user_id;
    },
    closeModal() {
      this.showDeleteModal = false;
    },
    deleteUser() {
      this.showDeleteModal = false;
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.usersApi +
        "/" +
        this.selectedUser;
      axios.delete(usersEndpoint).then(() => {
        this.getUsers();
      });
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
