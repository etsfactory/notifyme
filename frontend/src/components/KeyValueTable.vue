<template>
  <div class="keyvalue-table">
    <div v-for="(value, key, i) in data" :key="i" class="table">
      <span v-if="key !== disable" class="row">
        <div class="column">
          <div v-if="key === 'id'" class="column-container key">
            <strong>{{key}}</strong>
          </div>
          <div v-else class="column-container key">{{key}}</div>
        </div>
        <div class="column">
          <div v-if="key === 'id'" class="column-container data">
            <strong>{{value}}</strong>
          </div>
          <div v-else class="column-container data">{{value}}</div>
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
.keyvalue-table {
  width: 100%;
  color: #4f4f4f;
  margin-top: 4rem;
}
.row {
  display: grid;
  flex-wrap: wrap;
  grid-template-columns: 35% 65%;
  grid-auto-rows: 1fr;
  border-bottom: 1px solid #bdbdbd;
  padding: 0.4rem 0;
}
.key {
  font-weight: bold;
  text-transform: capitalize;
}
.column {
  width: 100%;
}
.column-container {
  padding: 0.3rem 1rem;
}
.data {
  font-size: 0.9rem;
}
@media (max-width: 1520px) {
  .row {
    grid-template-columns: 50% 50%;
  }
}
</style>
