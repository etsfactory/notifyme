<template>
  <div class="messages" :style="gridStyle">
    <div v-for="(item, i) in messages" :key="i" class="message" >
      <div class="info">
        <div>
          <div class="column-title">EXCHANGE</div>
          <div class="column-info">{{item.exchange}}</div>
        </div>
        <div>
          <div class="column-title">DATE</div>
          <div class="column-info">{{formatDate(item.date)}}</div>
        </div>
        <div>
          <div class="column-title">USERS</div>
          <div class="column-info users">
            ({{item.users.length}})
            <div class="popup">Users:
              <ul>
                <li v-for="(item, i) in item.users" :key="i">{{item}}</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="description">{{item.description}}</div>
      </div>
      <div class="button">
        <div class="arrow">
          <img svg-inline class="create-icon" src="../assets/icons/arrow.svg">
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import dayjs from "dayjs";

export default {
  name: "Messages",
  props: {
    columns: {
      type: Number,
      default: 3
    },
    messages: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    gridStyle() {
      console.log(this.columns);
      return {
        gridTemplateColumns: `repeat(${this.columns}, 1fr)`
      }
    },
  },
  methods: {
    formatDate(date) {
      return dayjs(date).format('YYYY/MM/DD - HH:mm:ss')
    }
  }
};
</script>

<style lang="scss" scoped>
.messages {
  display: grid;
  grid-column-gap: 3rem;
  grid-row-gap: 2rem;
  margin-top: 3rem;
}
.message {
  display: flex;
  justify-content: space-between;
  background: #f2f2f2;
  padding: 1.6rem;
  border-radius: 5px;
  align-items: center;
  position: relative;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}
.info {
  display: flex;
  width: 70%;
  justify-content: space-between;
  flex-wrap: wrap;
}
.description {
  margin-top: 1.5rem;
  width: 100%;
}
.column-title {
  color: $color-main;
}
.users {
  cursor: pointer;
  ul {
    padding: 0 2rem;
    margin: 0.5rem 0;
  }
}
.users:hover .popup {
  display: block;
}
.popup {
  display: none;
  position: absolute;
  bottom: -1rem;
  right: 3rem;
  background: white;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.2);
}
</style>
