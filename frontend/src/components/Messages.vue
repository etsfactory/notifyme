<template>
  <div class="messages">
    <div v-for="(item, i) in messages" :key="i" class="message" v-bind:style="{width: columns}">
      <div class="info">
        <div>
          <div class="column-title">EXCHANGE</div>
          <div class="column-info">{{item.exchange}}</div>
        </div>
        <div>
          <div class="column-title">DATE</div>
          <div class="column-info">{{item.date}}</div>
        </div>
        <div>
          <div class="column-title">USERS</div>
          <div class="column-info">{{item.users}}</div>
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
export default {
  name: "Messages",
  props: {
    messages: () => [],
    columns: "100%"
  }
};
</script>

<style lang="scss" scoped>
.messages {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  flex-wrap: wrap;
}
.message {
  width: 25%;
  display: flex;
  justify-content: space-between;
  background: #f2f2f2;
  padding: 1.6rem;
  border-radius: 5px;
  align-items: center;
  margin-top: 2rem;
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
</style>
