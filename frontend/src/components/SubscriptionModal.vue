<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <user-list v-if="users" :subscriptions="subscriptions" :users="users" @click="createUserSubscription"/>
      <bus-filter-list v-if="busFilters" :subscriptions="subscriptions" :bus-filters="busFilters" @click="createBusFilterSubscription"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserList from "@/components/UserList.vue";
import BusFilterList from "@/components/BusFilterList.vue";

export default {
  name: "SubscriptionModal",
  components: {
    UserList,
    BusFilterList
  },
  props: {
    visible: Boolean,
    type: String,
    id: String,
    subscriptions: {
      type: Array,
      default: []
    }
  },
  data: () => ({
    usersApi: "/users",
    busFiltersApi: "/bus_filters",
    users: null,
    busFilters: null
  }),
  methods: {
    close() {
      this.$emit("update:visible", false);
    },
    getUsers() {
      const usersEndpoint = process.env.VUE_APP_NOTIFYME_HOST + this.usersApi;
      axios.get(usersEndpoint).then(response => {
        this.users = response.data;
      });
    },
    getBusFilters() {
      const busFiltersEndpoint = process.env.VUE_APP_NOTIFYME_HOST + this.busFiltersApi;
      axios.get(busFiltersEndpoint).then(response => {
        this.busFilters = response.data;
      });
    },
    createUserSubscription(users) {
      let usersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.busFiltersApi +
        "/" +
        this.id +
        this.usersApi;
      axios.post(usersEndpoint, users).then(() => {
        this.$emit("click");
      });
    },
    createBusFilterSubscription(busFilters) {
      let busFiltersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.usersApi +
        "/" +
        this.id +
        this.busFiltersApi;
      axios.post(busFiltersEndpoint, busFilters).then(() => {
        this.$emit("click");
      });
    }
  },
  watch: {
    subscriptions() {
      this.users ? this.getUsers() : this.getBusFilters();
    }
  },
  created() {
    this.type === "users" ? this.getUsers() : this.getBusFilters();
  },
};
</script>

<style lang="scss" scoped>
</style>
