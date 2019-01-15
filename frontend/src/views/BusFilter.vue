<template>
  <div class="bus-filter">
    <div v-if="busFilter">
      <h1>
        <i class="fas fa-filter"></i> BusFilter
      </h1>
      <div class="bus-filter-container">
        <key-value-table class="info" :data="busFilter"/>
        <div class="buttons">
          <action-buttons @edit="showEditModal"></action-buttons>
        </div>
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
    busFilter: null,
    notifications: null,
    usersApi: "/users",
    busFiltersApi: "/bus_filters/",
    showConfirmModal: false,
    showCreateModal: false,
    showSubscriptionModal: false
  }),
  created() {
    this.getBusFilter(this.$route.params.id);
  },
  methods: {
    getBusFilter() {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.busFiltersApi +
        this.$route.params.id;
      axios.get(usersEndpoint).then(response => {
        this.busFilter = response.data;
        this.getBusNotifications();
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
    },
    subscriptionsCreated() {
      this.showSubscriptionModal = false;
      this.getBusNotifications();
    },
    getBusNotifications() {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.busFiltersApi +
        this.$route.params.id +
        this.usersApi;
      axios.get(usersEndpoint).then(response => {
        this.notifications = response.data;
      });
    },
    deleteSubscription() {
      this.showConfirmModal = false;
      const busFilterEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.busFiltersApi +
        this.busFilter.id +
        "/" +
        this.usersApi +
        "/" +
        this.selectedUser;
      axios.delete(busFilterEndpoint).then(() => {
        this.getUserNotifications();
      });
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
</style>
