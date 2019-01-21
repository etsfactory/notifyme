<template>
  <div class="user">
    <h1>
      <i class="fas fa-user"></i> User
    </h1>
    <error v-if="userError" :error="userError"/>
    <div v-if="user">
      <div class="user-container">
        <key-value-table :data="user" class="info"/>
        <div class="buttons">
          <action-buttons @edit="showEditModal" @remove="showDeleteUserModal = true"></action-buttons>
          <confirm-modal
            :visible.sync="showDeleteUserModal"
            @accept="deleteUser"
            subtitle="This action can not be undone"
          />
        </div>
      </div>
      <h2 class="notifications-title">
        <i class="fas fa-filter"></i> Suscribed to:
        <i class="fas fa-plus-circle create-icon" @click="showSubsModal"></i>
      </h2>
      <error v-if="busFilterError" :error="busFilterError"/>
      <div v-if="notifications" class="notifications">
        <bus-filters-table :bus-filters="notifications" @deleted="showDeleteModal"/>
        <confirm-modal
          :visible.sync="showConfirmModal"
          @accept="deleteSubscription"
          subtitle="This action can not be undone. This will delete the relation between user and bus filter but the bus filter won't be deleted"
        />
        <subscription-modal
          :visible.sync="showSubscriptionModal"
          type="busFilters"
          :id="user.id"
          :subscriptions="notifications"
          @click="subscriptionsCreated"
        />
        <create-user :model="user" :visible.sync="showCreateModal" :edit="true" @created="getUser"/>
      </div>
    </div>
  </div>
</template>

<script>
import usersApi from "@/logic/users";

import BusFiltersTable from "@/components/BusFiltersTable.vue";
import KeyValueTable from "@/components/KeyValueTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import ActionButtons from "@/components/ActionButtons.vue";
import CreateUser from "@/components/CreateUser.vue";
import SubscriptionModal from "@/components/SubscriptionModal.vue";
import Error from "@/components/Error.vue";

export default {
  name: "User",
  components: {
    BusFiltersTable,
    KeyValueTable,
    ConfirmModal,
    ActionButtons,
    CreateUser,
    SubscriptionModal,
    Error
  },
  data: () => ({
    user: null,
    notifications: null,
    showConfirmModal: false,
    showDeleteUserModal: false,
    selectedBusFilter: null,
    showCreateModal: false,
    showSubscriptionModal: false,
    userError: null,
    busFilterError: null
  }),
  computed: {
    nameToDisplay() {
      if ("name" in this.user) {
        return this.user.name;
      }
      return this.user.id;
    }
  },
  created() {
    this.getUser();
  },
  methods: {
    async getUser() {
      try {
        let response = await usersApi.get(this.$route.params.id);
        this.user = response.data;
        this.getUserNotifications(this.user.id);
      } catch (error) {
        this.userError = error.response;
      }
    },
    async getUserNotifications() {
      try {
        let response = await usersApi.getSubscriptions(this.user.id);
        this.notifications = response.data;
      } catch (error) {
        this.busFilterError = error.response;
      }
    },
    async deleteSubscription() {
      try {
        this.showConfirmModal = false;
        await usersApi.deleteSubscription(this.user.id, this.selectedBusFilter);
        this.getUserNotifications();
      } catch (error) {
        this.busFilterError = error.response;
      }
    },
    async deleteUser() {
      try {
        await usersApi.delete(this.user.id);
        this.$router.push("/users");
      } catch (error) {
        this.userError = error.response;
      }
    },
    showDeleteModal(bus_filter_id) {
      this.showConfirmModal = true;
      this.selectedBusFilter = bus_filter_id;
    },
    showEditModal() {
      this.showCreateModal = true;
    },
    showSubsModal() {
      this.showSubscriptionModal = true;
    },
    subscriptionsCreated() {
      this.showSubscriptionModal = false;
      this.getUserNotifications();
    }
  }
};
</script>

<style lang="scss" scoped>
.user {
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
.notifications-title {
  margin-top: 3rem;
}
.user-container {
  display: flex;
  align-items: center;
}
.buttons {
  width: 35%;
}
</style>