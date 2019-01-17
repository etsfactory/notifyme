<template>
  <div class="bus-filter">
    <div v-if="busFilter">
      <h1>
        <i class="fas fa-filter"></i> BusFilter
      </h1>
      <div class="bus-filter-container">
        <key-value-table class="info" :data="busFilter" disable="template_id"/>
        <div class="buttons">
          <action-buttons @edit="showEditModal"></action-buttons>
        </div>
      </div>
      <div v-if="template" class="template">
        <h2>
          <i class="fas fa-envelope"></i> Template:
        </h2>
        <template-table :remove="false" :templates="[template]" @deleted="showDeleteModal"/>
      </div>
      <div v-else class="template">
        No template asociated with this bus filter. All subscriptions created with this bus filter will be created with the default template specified in the config file.
      </div>
      <div v-if="notifications" class="users">
        <h2>
          <i class="fas fa-users"></i> Users suscribed to:
          <i class="fas fa-plus-circle create-icon" @click="showSubsModal"></i>
        </h2>
        <users-table :users="notifications" @deleted="showDeleteModal"/>
        <confirm-modal
          :visible.sync="showConfirmModal"
          @close="closeDeleteModal"
          @accept="deleteSubscription"
          subtitle="This action can not be undone. This will delete the relation between user and bus filter but the bus filter won't be deleted"
        />
        <subscription-modal
          :visible.sync="showSubscriptionModal"
          type="users"
          :id="busFilter.id"
          :subscriptions="notifications"
          @click="subscriptionsCreated"
        />
        <create-bus-filter
          :model="busFilter"
          :visible.sync="showCreateModal"
          :edit="true"
          @created="getBusFilter"
        />
      </div>
    </div>
  </div>
</template>

<script>
import busFiltersApi from "@/logic/bus_filters";

import UsersTable from "@/components/UsersTable.vue";
import TemplateTable from "@/components/TemplateTable.vue";
import KeyValueTable from "@/components/KeyValueTable.vue";
import ActionButtons from "@/components/ActionButtons.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateBusFilter from "@/components/CreateBusFilter.vue";
import SubscriptionModal from "@/components/SubscriptionModal.vue";

export default {
  name: "BusFilter",
  components: {
    UsersTable,
    TemplateTable,
    KeyValueTable,
    ActionButtons,
    ConfirmModal,
    CreateBusFilter,
    SubscriptionModal
  },
  data: () => ({
    busFilter: null,
    notifications: null,
    template: null,
    usersApi: "/users",
    busFiltersApi: "/bus_filters/",
    templatesApi: "/templates",
    showConfirmModal: false,
    showCreateModal: false,
    showSubscriptionModal: false
  }),
  created() {
    this.getBusFilter();
  },
  methods: {
    async getBusFilter() {
      let response = await busFiltersApi.get(this.$route.params.id);
      this.busFilter = response.data;
      this.getTemplate();
    },
    async getTemplate() {
      if (this.busFilter.template_id) {
        let response = await busFiltersApi.getTemplate();
        this.template = response.data;
      }
      this.getBusNotifications();
    },
    async getBusNotifications() {
      let response = await busFiltersApi.getSubscriptions(this.busFilter.id);
      this.notifications = response.data;
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
    },
    subscriptionsCreated() {
      this.showSubscriptionModal = false;
      this.getBusNotifications();
    },
    async deleteSubscription() {
      this.closeDeleteModal();
      await busFiltersApi.deleteSubscription(this.busFilter.id, this.selectedUser);
      this.getBusNotifications();

    },
    showSubsModal() {
      this.showSubscriptionModal = true;
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
.template {
  margin-top: 3rem;
}
.users {
  margin-top: 5rem;
}
.bus-filter-container {
  display: flex;
  align-items: center;
}
.buttons {
  width: 35%;
}
</style>
