<template>
  <div class="bus_filters">
    <h1>
      <i class="fas fa-filter"></i> Bus filters
      <i class="fas fa-plus-circle create-icon" @click="createBusFilter"></i>
    </h1>
    <error v-if="error" :error="error"/>
    <bus-filters-table v-if="busFilters" :bus-filters="busFilters" @deleted="showModal"/>
    <confirm-modal
      :visible.sync="showDeleteModal"
      @accept="deleteBusFilter"
      subtitle="CAUTION. If you delete a bus filter, all users suscribed to this bus filter will be unsuscribed. This action can not be undone"
    />
    <create-bus-filter :visible.sync="showCreateModal" @created="getBusFilters"/>
  </div>
</template>

<script>
import busFiltersApi from "@/logic/bus_filters";

import BusFiltersTable from "@/components/BusFiltersTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateBusFilter from "@/components/CreateBusFilter.vue";
import Error from "@/components/Error.vue";

export default {
  name: "Users",
  components: {
    BusFiltersTable,
    ConfirmModal,
    CreateBusFilter,
    Error
  },
  data: () => ({
    busFilters: null,
    showDeleteModal: false,
    selectedBusFilter: null,
    showCreateModal: false,
    error: null
  }),
  created() {
    this.getBusFilters();
  },
  methods: {
    async getBusFilters() {
      try {
        let response = await busFiltersApi.getAll();
        this.busFilters = response.data;
      } catch (error) {
        this.error = error.response;
      }
    },
    showModal(bus_filter_id) {
      this.showDeleteModal = true;
      this.selectedBusFilter = bus_filter_id;
    },
    async deleteBusFilter() {
      this.showDeleteModal = false;
      try {
        await busFiltersApi.delete(this.selectedBusFilter);
      } catch (error) {
        this.error = error.response;
      }
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
