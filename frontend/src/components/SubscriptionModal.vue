<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <error v-if="error" :error="error"/>
      <user-list
        v-if="users"
        :subscriptions="subscriptions"
        :users="users"
        @click="createBusFilterSubscription"
      />
      <bus-filter-list
        v-if="busFilters"
        :subscriptions="subscriptions"
        :bus-filters="busFilters"
        @click="createUserSubscription"
      />
    </div>
  </div>
</template>

<script>
import usersApi from "@/logic/users";
import busFiltersApi from "@/logic/bus_filters";

import UserList from "@/components/UserList.vue";
import BusFilterList from "@/components/BusFilterList.vue";

export default {
  name: "SubscriptionModal",
  components: {
    UserList,
    BusFilterList
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: ""
    },
    id: {
      type: String,
      default: ""
    },
    subscriptions: {
      type: Array,
      default: () => []
    }
  },
  data: () => ({
    users: null,
    busFilters: null,
    error: null
  }),
  watch: {
    subscriptions() {
      this.users ? this.getUsers() : this.getBusFilters();
    }
  },
  created() {
    this.type === "users" ? this.getUsers() : this.getBusFilters();
  },
  methods: {
    close() {
      this.$emit("update:visible", false);
    },
    async getUsers() {
      try {
        let response = await usersApi.getAll();
        this.users = response.data;
      } catch (error) {
        this.error = error.response;
      }
    },
    async getBusFilters() {
      try {
        let response = await busFiltersApi.getAll();
        this.busFilters = response.data;
      } catch (error) {
        this.error = error.response;
      }
    },
    async createUserSubscription(busFilters) {
      try {
        await usersApi.createSubscription(this.id, busFilters);
        this.$emit("click");
      } catch (error) {
        this.error = error.response;
      }
    },
    async createBusFilterSubscription(users) {
      try {
        await busFiltersApi.createSubscription(this.id, users);
        this.$emit("click");
      } catch (error) {
        this.error = error.response;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
