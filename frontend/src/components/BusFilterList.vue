<template>
  <div class="users-subscription">
    <ul class="user-list">
      Bus filters not suscribed to this user:
      <li v-for="(busFilter,i) in busFiltersFiltered" :key="i" class="user">
        <div class="info">
          <div class="name">
            <span class="id">{{busFilter.exchange}}</span>
            {{busFilter.key}}
          </div>
          <div>{{busFilter.description}}</div>
        </div>
        <div class="button">
          <div class="toggler">
            <toggler :toggled="isSuscribed(busFilter.id)" @click="select(busFilter, $event)"/>
          </div>
        </div>
      </li>
    </ul>
    <div class="center">
      <button class="button-main" @click="$emit('click', selectedbusFilters)">Create</button>
    </div>
  </div>
</template>

<script>
import Toggler from "@/components/Toggler.vue";
export default {
  name: "BusFilterList",
  components: {
    Toggler
  },
  props: {
    busFilters: {
      type: Array,
      default: []
    },
    subscriptions: {
      type: Array,
      default: []
    }
  },
  data: () => ({
    selectedbusFilters: [],
    busFilterSelected: false,
    busFiltersFiltered: []
  }),
  methods: {
    select(busFilter, toggled) {
      if (toggled) {
        this.selectedbusFilters.push(busFilter);
      } else {
        let index = this.selectedbusFilters.indexOf(busFilter);
        if (index > -1) {
          this.selectedbusFilters.splice(index, 1);
        }
      }
      this.busFilterSelected = toggled;
    },
    isSuscribed(id) {
       return this.subscriptions.some(item => item.id === id);
    },
    filterbusFilters() {
      this.busFiltersFiltered = this.busFilters.filter((item) => !this.isSuscribed(item.id) );
    }
  },
  created() {
    this.filterbusFilters();
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
