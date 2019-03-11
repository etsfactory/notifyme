<template>
  <div class="bus-filter">
    <h1>
      <i class="fas fa-filter"></i> BusFilter
    </h1>
    <error v-if="userError" :error="userError"/>
    <div v-if="busFilter">
      <div class="bus-filter-container">
        <key-value-table class="info" :data="busFilter" disable="template_id"/>
        <div class="buttons">
          <action-buttons @edit="showEditModal" @remove="showDeleteBusFilter = true"></action-buttons>
          <confirm-modal
            :visible.sync="showDeleteBusFilter"
            @accept="deleteBusFilter"
            subtitle="This action can not be undone."
          />
        </div>
      </div>
      <h2 class="templates-title">
        <i class="fas fa-envelope"></i> Template:
      </h2>
      <div v-if="template" class="template">
        <error v-if="busFilterError" :error="busFilterError"/>
        <template-table :remove="false" :templates="[template]"/>
      </div>
      <div v-else class="template">
        No template asociated with this bus filter. All subscriptions created with this bus filter will be created with the default template specified in the config file.
        <button
          class="button-main button-template"
          @click="showTemplateCreate"
        >Create template</button>
        <create-template
          :visible.sync="showTemplateModal"
          :http-call="false"
          @created="createTemplate"
        />
      </div>
      <h2 class="notifications-title">
        <i class="fas fa-users"></i> Users suscribed to:
        <i class="fas fa-plus-circle create-icon" @click="showSubsModal"></i>
      </h2>
      <error v-if="userError" :error="userError"/>
      <div v-if="notifications" class="notifications">
        <users-table :users="notifications" @deleted="showDeleteModal"/>
        <confirm-modal
          :visible.sync="showConfirmModal"
          @accept="deleteSubscription"
          subtitle="This action can not be undone. This will delete the relation between user and bus filter but the bus filter won't be deleted"
        />
        <subscription-modal
          v-if="showSubscriptionModal"
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
import CreateTemplate from "@/components/CreateTemplate.vue";
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
    CreateTemplate,
    SubscriptionModal
  },
  data: () => ({
    busFilter: null,
    notifications: null,
    template: null,
    showConfirmModal: false,
    showCreateModal: false,
    showTemplateModal: false,
    showDeleteBusFilter: false,
    showSubscriptionModal: false,
    busFilterError: null,
    userError: null,
    templateError: null
  }),
  created() {
    this.getBusFilter();
  },
  methods: {
    async getBusFilter() {
      try {
        let response = await busFiltersApi.get(this.$route.params.id);
        this.busFilter = response.data;
        this.getTemplate();
      } catch (error) {
        this.busFilterError = error.response;
      }
    },
    async getTemplate() {
      try {
        if (this.busFilter.template_id) {
          let response = await busFiltersApi.getTemplate(this.busFilter.id);
          this.template = response.data;
        }
        this.getBusNotifications();
      } catch (error) {
        this.templateError = error.response;
      }
    },
    async getBusNotifications() {
      try {
        let response = await busFiltersApi.getSubscriptions(this.busFilter.id);
        this.notifications = response.data;
      } catch (error) {
        this.userError = error.response;
      }
    },
    async createTemplate(template) {
      try {
        await busFiltersApi.createTemplate(this.busFilter.id, template);
        this.showTemplateModal = false;
        let response = await busFiltersApi.getTemplate(this.busFilter.id);
        this.template = response.data;
      } catch (error) {
        this.templateError = error.response;
      }
    },
    async deleteBusFilter() {
      this.showDeleteBusFilter = false;
      try {
        await busFiltersApi.delete(this.busFilter.id);
        this.$router.push("/bus_filters");
      } catch (error) {
        this.busFilter = error.response;
      }
    },
    showEditModal() {
      this.showCreateModal = true;
    },
    showDeleteModal(id) {
      this.showConfirmModal = true;
      this.selectedUser = id;
    },
    showTemplateCreate() {
      this.showTemplateModal = true;
    },
    subscriptionsCreated() {
      this.showSubscriptionModal = false;
      this.getBusNotifications();
    },
    async deleteSubscription() {
      this.showConfirmModal = false;
      await busFiltersApi.deleteSubscription(
        this.busFilter.id,
        this.selectedUser
      );
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
.templates-title {
  margin-top: 3rem;
}
.notifications-title {
  margin-top: 3rem;
}
.bus-filter-container {
  display: flex;
  align-items: center;
}
.buttons {
  width: 35%;
}
.button-template {
  display: block;
  margin: 1rem 0;
}
</style>
