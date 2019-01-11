<template>
  <sorteable-table :columns="columns" :data="busFilters" class="users-table">
    <template slot="row" slot-scope="busFilter">
      <td>{{busFilter.row.id}}</td>
      <td>{{busFilter.row.exchange}}</td>
      <td>{{busFilter.row.exchange_type}}</td>
      <td v-if="busFilter.row.category">{{busFilter.row.category}}</td>
      <td class="multiline" v-if="busFilter.row.description">{{busFilter.row.description}}</td>
      <td class="actions">
        <i class="far fa-eye icon" @click="navigateToBusFilter(busFilter.row.id)"></i>
        <i class="far fa-trash-alt icon" @click="deleteBusFilter(busFilter.row.id)"></i>
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
    }
  },
  data: () => ({
    columns: [
      { text: "Id", key: "id", sorteable: true },
      { text: "Exchange", key: "exchange", sorteable: true },
      { text: "Exchange Type", key: "exchange_type", sorteable: false }
    ]
  }),
  created() {
    if ("category" in this.busFilters[0]) {
      this.addColumn("Category", "category", true);
    }
    if ("description" in this.busFilters[0]) {
      this.addColumn("Description", "description", true, "multiline");
    }
    this.addColumn("Actions", "actions", false, "actions");
  },
  methods: {
    navigateToBusFilter(bus_filter_id) {
      this.$router.push({ name: "bus_filter", params: { id: bus_filter_id } });
    },
    addColumn(text, key, sorteable, className) {
      this.columns.push({
        text: text,
        key: key,
        sorteable: sorteable,
        class: className
      });
    },
    deleteBusFilter(bus_filter_id) {
      this.$emit("deleted", bus_filter_id);
    }
  }
};
</script>

<style lang="scss" scoped>
.users-table /deep/.actions {
  text-align: center !important;
}
.users-table /deep/.multiline {
  white-space: pre-line;
  word-wrap: break-word;
}
.icon {
  padding: 0 3rem;
  cursor: pointer;
  &:hover {
    color: $color-main-dark;
  }
}
</style>
