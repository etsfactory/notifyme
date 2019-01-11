<template>
  <div class="bus_filters">
    <h1>
      <i class="fas fa-filter"></i> Bus filters
    </h1>
    <bus-filters-table v-if="busFilters" :bus-filters="busFilters" @deleted="deleteBusFilter"/>
    <confirm-modal :visible.sync="confirmVisible" @close="closeModal"/>
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
    confirmVisible: false
  }),
  methods: {
    getBusFilters() {
      const busFilterEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST + this.busFiltersApi;
      axios.get(busFilterEndpoint).then(response => {
        this.busFilters = response.data;
      });
    },
    deleteBusFilter(bus_filter_id) {
      this.confirmVisible = true;
    },
    closeModal() {
      this.confirmVisible = false;
    }
  },
  created() {
    this.getBusFilters();
  }
};
</script>

<style lang="scss" scoped>
</style>
