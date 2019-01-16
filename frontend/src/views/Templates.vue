<template>
  <div class="users">
    <h1>
      <i class="fas fa-envelope"></i> Templates
      <i class="fas fa-plus-circle create-icon" @click="createUser"></i>
    </h1>
    <template-table v-if="users" :templates="users" @deleted="showModal"/>
    <confirm-modal :visible.sync="showDeleteModal" @close="closeModal" @accept="deleteUser"/>
    <create-template :visible.sync="showCreateModal" @created="getTemplates"/>
  </div>
</template>

<script>
import axios from "axios";
import TemplateTable from "@/components/TemplateTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateTemplate from "@/components/CreateTemplate.vue";

export default {
  name: "Templates",
  components: {
    TemplateTable,
    ConfirmModal,
    CreateTemplate
  },
  data: () => ({
    usersApi: "/templates",
    users: null,
    showDeleteModal: false,
    selectedUser: null,
    showCreateModal: false
  }),
  created() {
    this.getTemplates();
  },
  methods: {
    getTemplates() {
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
