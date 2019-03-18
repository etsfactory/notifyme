<template>
  <div class="users-subscription">
    <div class="user-list">Users not suscribed to this bus filter:
      <div class="warning" v-if="usersFiltered.length === 0">
        <strong>No users found.</strong> Please go to
        <router-link to="/users">users page</router-link>and create some
      </div>
      <ul class="list">
        <li v-for="(user,i) in usersFiltered" :key="i" class="user">
          <div class="info">
            <div class="name">
              <span class="id">{{user.id}}</span>
              {{user.name}}
            </div>
            <div>{{user.email}}</div>
          </div>
          <div class="button">
            <div class="toggler">
              <toggler :toggled="isSuscribed(user.id)" @click="select(user, $event)"/>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <div class="center">
      <button
        v-if="usersFiltered.length !== 0"
        class="button-main button-submit"
        @click="$emit('click', selectedUsers)"
      >
        <img svg-inline class="icon create-icon" src="../assets/icons/plus.svg"> Add users
      </button>
    </div>
  </div>
</template>

<script>
import Toggler from "@/components/Toggler.vue";
export default {
  name: "UserList",
  components: {
    Toggler
  },
  props: {
    users: {
      type: Array,
      default: () => []
    },
    subscriptions: {
      type: Array,
      default: () => []
    }
  },
  data: () => ({
    selectedUsers: [],
    userSelected: false
  }),
  computed: {
    usersFiltered() {
      return this.users.filter(item => !this.isSuscribed(item.id));
    }
  },
  watch: {
    users() {
      this.selectedUsers = [];
    }
  },
  methods: {
    select(user, toggled) {
      if (toggled) {
        this.selectedUsers.push(user);
      } else {
        let index = this.selectedUsers.indexOf(user);
        if (index > -1) {
          this.selectedUsers.splice(index, 1);
        }
      }
      this.userSelected = toggled;
    },
    isSuscribed(user_id) {
      return this.subscriptions.some(item => item.id === user_id);
    }
  }
};
</script>

<style lang="scss" scoped>
.user-list,
.users-subscription {
  width: 100%;
  margin: 0;
}
.user-list {
  overflow-y: auto;
  max-height: 700px;
  padding: 1rem 0;
}
.user {
  width: 48%;
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  background: #f2f2f2;
  border-radius: 5px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}
.info {
  width: 80%;
  padding: 1rem;
}
.name {
  font-size: 1.2rem;
}
.button {
  padding: 1rem;
}
.id {
  font-weight: bold;
  padding-right: 10px;
}
.toggler {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.sub-button {
  margin-top: 3rem;
}
.list {
  display: flex;
  justify-content: space-between;
  padding: 0;
}
</style>
