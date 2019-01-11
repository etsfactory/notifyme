<template>
  <div class="bus_filters">
    <h1>
      <i class="fas fa-filter"></i> Bus filters
    </h1>
    <bus-filters-table v-if="busFilters" :bus-filters="busFilters" @deleted="showModal"/>
    <confirm-modal :visible.sync="openModal" @close="closeModal" @accept="deleteBusFilter" subtitle="CAUTION. If you delete a bus filter, all users suscribed to this bus filter will be unsuscribed. This action can not be undone"/>
  </div>
</template>

<script>
import axios from "axios";
import BusFiltersTable from "@/components/BusFiltersTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";

export default {
  name: "Users",
  components: {
    BusFiltersTable,
    ConfirmModal
  },
  data: () => ({
    busFiltersApi: "/bus_filters",
    busFilters: null,
    openModal: false,
    selectedBusFilter: null
  }),
  created() {
    this.getBusFilters();
  },
  methods: {
    getBusFilters() {
      const busFilterEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST + this.busFiltersApi;
      axios.get(busFilterEndpoint).then(response => {
        this.busFilters = response.data;
      });
    },
    showModal(bus_filter_id) {
      this.openModal = true;
      this.selectedBusFilter = bus_filter_id;
    },
    closeModal() {
      this.openModal = false;
    },
    deleteBusFilter() {
      this.openModal = false;
      const busFilterEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.busFiltersApi +
        "/" +
        this.selectedBusFilter;
      axios.delete(busFilterEndpoint).then(() => {
        this.getBusFilters();
      });
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
