<template>
  <div>
    <error v-if="userError" :error="userError"/>
    <div v-if="user">
      <the-header>
        <template slot="title">User</template>
        <template slot="buttons">
          <router-link to="/bus_filters" class="link">
            <i class="fas fa-chevron-left"></i>Back to users
          </router-link>
        </template>
      </the-header>
      <div class="user">
        <div class="user-container">
          <div class="buttons">
            <action-buttons @edit="showEditModal" @remove="showDeleteUserModal = true"></action-buttons>
            <confirm-modal
              :visible.sync="showDeleteUserModal"
              @accept="deleteUser"
              subtitle="This action can not be undone"
            />
          </div>
          <key-value-table :data="user" class="info"/>
        </div>
        <div class="right">
          <div class="right-title">
            <h2 class="notifications-title">Suscribed to:</h2>
            <button class="button-create" @click="showSubsModal">
              <img svg-inline class="create-icon" src="../assets/icons/plus.svg"> New subscription
            </button>
          </div>
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
    </div>
  </div>
</template>

<script>
import usersApi from "@/logic/users";

import BusFiltersTable from "@/components/BusFiltersTable.vue";
import KeyValueTable from "@/components/KeyValueTable.vue";
import TheHeader from "@/components/TheHeader.vue";
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
    TheHeader,
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
      this.showConfirmModal = false;
      try {
        await usersApi.deleteSubscription(this.user.id, this.selectedBusFilter);
        this.getUserNotifications();
      } catch (error) {
        this.busFilterError = error.response;
      }
    },
    async deleteUser() {
      this.showDeleteUserModal = false;
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
.header {
  width: 24%;
}
.user {
  position: relative;
  display: flex;
}
.notifications-table /deep/.actions {
  text-align: center !important;
}
.icon {
  padding: 0 3rem;
  cursor: pointer;
  &:hover {
    color: $color-secundary;
  }
}
.user-container {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-right: 3rem;
}
.buttons {
  width: 100%;
}
.right {
  width: 75%;
  margin-top: -78px;
}
.fa-chevron-left {
  color: $color-main;
  margin-right: 0.5rem;
}
.link {
  text-decoration: none;
  color: #828282;
}
.right-title {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.button-create {
  background: transparent;
  border: none !important;
  cursor: pointer;
  color: #333333;
  border-radius: 3px;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  font-size: 0.8rem;
  height: 45px;
  padding: 0 1rem;
  &:hover {
    background: rgba(0, 0, 0, 0.04);
  }
}
@media (max-width: 1520px) {
  .user-container {
    width: 30%;
  }
  .right {
    width: 70%;
  }
}
</style>
