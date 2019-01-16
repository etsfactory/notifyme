<template>
  <div class="users-subscription">
    <ul class="user-list">
      Users not suscribed to this bus filter:
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
    <div class="center">
      <button class="button-main" @click="$emit('click', selectedUsers)">Create</button>
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
      default: []
    },
    subscriptions: {
      type: Array,
      default: []
    }
  },
  data: () => ({
    selectedUsers: [],
    userSelected: false,
    usersFiltered: []
  }),
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
    },
    filterUsers() {
      this.usersFiltered = this.users.filter((item) => !this.isSuscribed(item.id) );
    }
  },
  created() {
    this.filterUsers();
  }
};
</script>

<style lang="scss" scoped>
.user-list,
.users-subscription {
  width: 100%;
  margin: 0;
  padding: 0;
}
.user {
  display: flex;
  justify-content: space-between;
  width: 100%;
  background: rgba(0, 0, 0, 0.03);
  margin-top: 1rem;
}
.info {
  width: 80%;
  padding: 1rem;
}
.button {
  width: 15%;
}
.name {
  font-size: 1.2rem;
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
</style>
