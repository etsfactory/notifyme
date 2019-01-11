<template>
  <div class="user">
    <div v-if="user">
      <h1>
        <i class="fas fa-user"></i> User
      </h1>
      <key-value-table :data="user" class="info"/>
      <div v-if="notifications" class="notifications">
        <h2>
          <i class="fas fa-filter"></i> Suscribed to:
        </h2>
        <bus-filters-table :bus-filters="notifications" @deleted="showModal"/>
        <confirm-modal :visible.sync="openModal" @close="closeModal" @accept="deleteSubscription" subtitle="This action can not be undone. This will delete the relation between user and bus filter but the bus filter won't be deleted"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import BusFiltersTable from "@/components/BusFiltersTable.vue";
import KeyValueTable from "@/components/KeyValueTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";

export default {
  name: "User",
  components: {
    BusFiltersTable,
    KeyValueTable,
    ConfirmModal
  },
  data: () => ({
    user: null,
    notifications: null,
    usersApi: "/users/",
    notificationsApi: "/bus_filters",
    openModal: false,
    selectedBusFilter: null
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
    this.getUser(this.$route.params.id);
  },
  methods: {
    getUser(id) {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST + this.usersApi + id;
      axios.get(usersEndpoint).then(response => {
        this.user = response.data;
        this.getUserNotifications(this.$route.params.id);
      });
    },
    getUserNotifications() {
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.usersApi +
        this.user.id +
        this.notificationsApi;
      axios.get(usersEndpoint).then(response => {
        this.notifications = response.data;
      });
    },
    showModal(bus_filter_id) {
      this.openModal = true;
      this.selectedBusFilter = bus_filter_id;
    },
    closeModal() {
      this.openModal = false;
    },
    deleteSubscription() {
      this.openModal = false;
      const usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.usersApi +
        this.user.id +
        this.notificationsApi +
        "/" +
        this.selectedBusFilter;
      axios.delete(usersEndpoint).then(() => {
        this.getUserNotifications();
      });
    }
  }
};
</script>

<style lang="scss" scoped>
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
  width: 50%;
}
.notifications {
  margin-top: 3rem;
}
</style>
