<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <user-list v-if="users" :subscriptions="subscriptions" :users="users" @click="createUserSubscription"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserList from "@/components/UserList.vue";

export default {
  name: "SubscriptionModal",
  components: {
    UserList
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
    users: null
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
    }
  },
  created() {
    this.type === "users" ? this.getUsers() : this.getBusFilters();
  }
};
</script>

<style lang="scss" scoped>
</style>
