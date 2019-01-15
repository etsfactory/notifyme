<template>
  <div class="bus-filter">
    <div v-if="template">
      <h1>
        <i class="fas fa-envelope"></i> Template
      </h1>
      <div class="bus-filter-container">
        <key-value-table class="info" :data="template" disable="text"/>
        <div class="buttons">
          <action-buttons @edit="showEditModal"></action-buttons>
        </div>
      </div>
      <div class="text">
        <h2>Body for the email:</h2>
       <span>{{template.text}}></span>
        <pre v-highlightjs>
          <code class="html">
            {{template.text}}
          </code>
        </pre>
      </div>
      <create-bus-filter
        :model="template"
        :visible.sync="showCreateModal"
        :edit="true"
        @created="getTemplate"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UsersTable from "@/components/UsersTable.vue";
import KeyValueTable from "@/components/KeyValueTable.vue";
import ActionButtons from "@/components/ActionButtons.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateBusFilter from "@/components/CreateBusFilter.vue";
import SubscriptionModal from "@/components/SubscriptionModal.vue";

export default {
  name: "BusFilter",
  components: {
    UsersTable,
    KeyValueTable,
    ActionButtons,
    ConfirmModal,
    CreateBusFilter,
    SubscriptionModal
  },
  data: () => ({
    template: null,
    templatesApi: "/templates/",
    showConfirmModal: false,
    showCreateModal: false,
    showSubscriptionModal: false
  }),
  created() {
    this.getTemplate(this.$route.params.id);
  },
  methods: {
    getTemplate() {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.templatesApi +
        this.$route.params.id;
      axios.get(usersEndpoint).then(response => {
        this.template = response.data;
      });
    },
    showEditModal() {
      this.showCreateModal = true;
    },
    showDeleteModal(id) {
      this.showConfirmModal = true;
      this.selectedUser = id;
    },
    closeDeleteModal() {
      this.showConfirmModal = false;
    }
  }
};
</script>

<style lang="scss" scoped>
.bus-filter {
  position: relative;
}
.notifications-table /deep/.actions {
  text-align: center !important;
}
.icon {
  padding: 0 3rem;
  cursor: pointer;
  &:hover {
    color: $color-main-dark;
  }
}
.info {
  width: 40%;
}
.users {
  margin-top: 3rem;
}
.bus-filter-container {
  display: flex;
  align-items: center;
}
.buttons {
  width: 35%;
}
.text {
  margin-top: 2rem;
}
</style>
