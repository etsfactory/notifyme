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

import Error from "@/components/Error.vue";

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
    users: null,
    busFilters: null,
    error: null
  }),
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
    async createUserSubscription(users) {
      try {
        await usersApi.createSubscription(this.id, this.busFilters);
        this.$emit("click");
      } catch (error) {
        this.error = error.response;
      }
    },
    async createBusFilterSubscription(busFilters) {
      try {
        await busFiltersApi.createSubscription(this.id, this.users);
        this.$emit("click");
      } catch (error) {
        this.error = error.response;
      }
    }
  },
  watch: {
    subscriptions() {
      this.users ? this.getUsers() : this.getBusFilters();
    }
  },
  created() {
    this.type === "users" ? this.getUsers() : this.getBusFilters();
  }
};
</script>

<style lang="scss" scoped>
</style>
