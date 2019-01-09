<template>
  <table class="list">
    <thead class="table-header">
      <slot name="column">
        <th
          v-for="(column, i) in columns"
          :colspan="columnColSpan(column)"
          :key="i"
          @click="sort(column)"
          :class="[
            'header',
            {'sorteable': isSorteable(column)},
            arrow(column),
            columnClass(column)
          ]"
        >
          <template>{{getColumnName(column)}}</template>
        </th>
      </slot>
    </thead>
    <tbody>
      <template v-if="isObject(data)">
        <tr v-for="(item, i) in sortedData" :key="i">
          <slot name="row" :row="item">
            <td
              v-for="(column, j) in columns"
              :key="j"
              v-if="hasValue(item, column)"
            >{{itemValue(item, column)}}</td>
          </slot>
        </tr>
      </template>
      <tr v-else>
        <slot name="row" :row="data">{{data}}</slot>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <slot name="footer"></slot>
      </tr>
    </tfoot>
  </table>
</template>
<script>
export default {
  name: "SorteableTable",
  props: {
    columns: Array,
    data: Array | Number | String,
    filterKey: String
  },
  data: () => ({
    currentSort: "",
    currentSortDir: "asc"
  }),
  methods: {
    sort(c) {
      console.log(c);
      let column = this.getColumnKey(c);
      if (column === this.currentSort && this.isSorteable(c)) {
        this.currentSortDir = this.currentSortDir === "asc" ? "desc" : "asc";
      }
      this.currentSort = column;
    },
    hasValue(item, c) {
      let column = this.getColumnKey(c);
      return item[column.toLowerCase()] !== "undefined";
    },
    itemValue(item, c) {
      let column = this.getColumnKey(c);
      return item[column.toLowerCase()];
    },
    getColumnKey(c) {
      if (this.isObject(c)) {
        if (c.key) {
          return c.key;
        } else {
          return c.text;
        }
      } else {
        return c;
      }
    },

    getColumnName(c) {
      if (this.isObject(c)) {
        return c.text;
      } else {
        return c;
      }
    },

    isObject(o) {
      return typeof o === "object";
    },

    arrow(c) {
      let column = this.getColumnKey(c);
      if (this.currentSort === column && this.isSorteable(c)) {
        if (this.currentSortDir === "asc") return "headerSortDown";
        if (this.currentSortDir === "desc") return "headerSortUp";
      }
    },
    columnClass(c) {
      if (c.class) {
        return c.class;
      }
    },

    columnColSpan(c) {
      if (c.colspan) {
        return c.colspan;
      } else {
        return 1;
      }
    },
    isSorteable(c) {
      if (!this.isObject(c)) return false;
      return typeof c.sorteable === "undefined" ? true : c.sorteable;
    },
    formatToCompare(x) {
      if (typeof x === "number") {
        return x;
      } else if (typeof x === "string") {
        return x.toLowerCase();
      }
      return x;
    },

    filterData(data) {
      if (this.filterKey && this.filterKey !== "") {
        data = data.filter(row => {
          return Object.keys(row).some(key => {
            return (
              String(row[key])
                .toLowerCase()
                .indexOf(this.filterKey) > -1
            );
          });
        });
      }

      return data;
    }
  },
  computed: {
    sortedData() {
      if (this.data) {
        let dataAux = this.data;
        console.log(this.data);
        dataAux = this.filterData(dataAux);
        if (typeof dataAux !== "undefined" && typeof dataAux === "object") {
          return dataAux.sort((a, b) => {
            let x = a[this.currentSort];
            let y = b[this.currentSort];

            let modifier = 1;
            if (this.currentSortDir === "desc") modifier = -1;

            let compare1 = this.formatToCompare(x);
            let compare2 = this.formatToCompare(y);

            if (compare1 < compare2) return -1 * modifier;
            if (compare1 > compare2) return 1 * modifier;

            if (compare1 === "-" || !compare1) return -1 * modifier;
            if (compare2 === "-" || !compare2) return 1 * modifier;

            return 0;
          });
        }
      }
    }
  }
};
</script>
<style scoped lang="scss">
th {
  padding-right: 25px !important;
}

.sorteable {
  cursor: pointer;
}
.header {
  border-bottom: 2px solid $color-main;
  vertical-align: middle;
  position: relative;
  text-align: left;
}
.headerSortUp::after {
  content: "▼";
  font-size: 8px;
  position: absolute;
  right: 5px;
  top: 30%;
}
.headerSortDown::after {
  content: "▲";
  font-size: 8px;
  position: absolute;
  right: 5px;
  top: 30%;
}
</style>
