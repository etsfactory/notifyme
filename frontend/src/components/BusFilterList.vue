<template>
  <div class="bus-filter-subscription">
    <ul class="bus-filter-list">Bus filters not suscribed to this user:
      <div class="warning" v-if="busFiltersFiltered.length === 0">
        <strong>No filters found.</strong> Please go to
        <router-link to="/bus_filters">filters page</router-link>and create some
      </div>
      <li v-for="(busFilter,i) in busFiltersFiltered" :key="i" class="bus-filter">
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
      <button
        v-if="busFiltersFiltered.length !== 0"
        class="button-main button-submit"
        @click="$emit('click', selectedbusFilters)"
      >Add bus filters</button>
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
      default: () => []
    },
    subscriptions: {
      type: Array,
      default: () => []
    }
  },
  data: () => ({
    selectedbusFilters: [],
    busFilterSelected: false
  }),
  computed: {
    busFiltersFiltered() {
      return this.busFilters.filter(item => !this.isSuscribed(item.id));
    }
  },
  watch: {
    busFilters() {
      this.selectedbusFilters = [];
    }
  },
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
    }
  }
};
</script>

<style lang="scss" scoped>
.bus-filter-list,
.bus-filter-subscription {
  width: 100%;
  margin: 0;
  padding: 0;
}
.bus-filter-list {
  overflow-y: auto;
  max-height: 700px;
}
.bus-filter {
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
