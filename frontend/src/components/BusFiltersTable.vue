<template>
  <sorteable-table :columns="columns" :data="busFilters" class="users-table">
    <template slot="row" slot-scope="busFilter">
      <td>{{busFilter.row.id}}</td>
      <td>{{busFilter.row.exchange}}</td>
      <td>{{busFilter.row.exchange_type}}</td>
      <td>{{busFilter.row.key}}</td>
      <td>{{busFilter.row.category}}</td>
      <td class="multiline">{{busFilter.row.description}}</td>
      <td class="actions">
        <img svg-inline class="icon" src="../assets/icons/eye.svg" @click="navigateToBusFilter(busFilter.row.id)">
        <img v-if="!disableDelete" svg-inline class="icon trash" src="../assets/icons/trash.svg" @click="deleteBusFilter(busFilter.row.id)">
      </td>
    </template>
  </sorteable-table>
</template>

<script>
import SorteableTable from "@/components/SorteableTable.vue";

export default {
  name: "BusFiltersTable",
  components: {
    SorteableTable
  },
  props: {
    busFilters: {
      type: Array,
      required: true
    },
    disableDelete: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    columns: [
      { text: "ID", key: "id", sorteable: true },
      { text: "Exchange", key: "exchange", sorteable: true },
      { text: "Exchange Type", key: "exchange_type", sorteable: true },
      { text: "Routing key", key: "key", sorteable: true },
      { text: "Category", key: "category", sorteable: true },
      { text: "Description", key: "description", sorteable: true },
      { text: "", key: "actions", sorteable: false }
    ]
  }),
  methods: {
    navigateToBusFilter(bus_filter_id) {
      this.$router.push({ name: "bus_filter", params: { id: bus_filter_id } });
    },
    deleteBusFilter(bus_filter_id) {
      this.$emit("deleted", bus_filter_id);
    }
  }
};
</script>

<style lang="scss" scoped>
.users-table /deep/.multiline {
  white-space: pre-line;
  word-wrap: break-word;
}
</style>
