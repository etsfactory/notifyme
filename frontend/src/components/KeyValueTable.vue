<template>
  <div class="keyvalue-table">
    <div v-for="(value, key, i) in data" :key="i" class="table">
      <span v-if="key !== disable" class="row">
        <div class="column">
          <div v-if="key === 'id'" class="column-container key"><strong>{{key}}</strong></div>
          <div v-else class="column-container key">{{key}}</div>
        </div>
        <div class="column">

          <div v-if="key === 'id'" class="column-container"><strong>{{value}}</strong></div>
          <div v-else class="column-container">{{value}}</div>
        </div>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "KeyValueTable",
  props: {
    data: {
      type: Object,
      required: true
    },
    disable: {
      type: String,
      default: ""
    }
  }
};
</script>

<style lang="scss" scoped>
.row {
  display: grid;
  flex-wrap: wrap;
  grid-template-columns: 1fr 1fr;
  grid-auto-rows: 1fr;
  border-bottom: 1px solid grey;
  border-right: 3px solid $color-main;
  border-left: 3px solid $color-main;
  & > .column:first-child {
    border-right: 3px solid $color-main;
  }
}
.key {
  color: $color-main-dark;
}
.column {
  width: 100%;
}
.column-container {
  padding: 0.3rem 1rem;
}
</style>
