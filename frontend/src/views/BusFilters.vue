<template>
  <div class="bus_filters">
    <h1>
      <i class="fas fa-filter"></i> Bus filters
      <i class="fas fa-plus-circle create-icon" @click="createBusFilter"></i>
    </h1>
    <bus-filters-table v-if="busFilters" :bus-filters="busFilters" @deleted="showModal"/>
    <confirm-modal :visible.sync="showDeleteModal" @close="closeModal" @accept="deleteBusFilter" subtitle="CAUTION. If you delete a bus filter, all users suscribed to this bus filter will be unsuscribed. This action can not be undone"/>
    <create-bus-filter :visible.sync="showCreateModal" @created="getBusFilters"/>
  </div>
</template>

<script>
import busFiltersApi from "@/logic/bus_filters";

import BusFiltersTable from "@/components/BusFiltersTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateBusFilter from "@/components/CreateBusFilter.vue";

export default {
  name: "Users",
  components: {
    BusFiltersTable,
    ConfirmModal,
    CreateBusFilter
  },
  data: () => ({
    busFilters: null,
    showDeleteModal: false,
    selectedBusFilter: null,
    showCreateModal: false,
  }),
  created() {
    this.getBusFilters();
  },
  methods: {
    async getBusFilters() {
      let response = await busFiltersApi.getAll();
      this.busFilters = response.data;
    },
    showModal(bus_filter_id) {
      this.showDeleteModal = true;
      this.selectedBusFilter = bus_filter_id;
    },
    closeModal() {
      this.showDeleteModal = false;
    },
    async deleteBusFilter() {
      this.closeModal();
      await busFiltersApi.delete(this.selectedBusFilter);
      this.getBusFilters();
    },
    createBusFilter() {
      this.showCreateModal = true;
    }
  }
};
</script>

<style lang="scss" scoped>
.bus_filters {
  position: relative;
}
</style>
