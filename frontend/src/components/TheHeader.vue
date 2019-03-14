<template>
  <header class="header">
    <h1 class="title">
      <slot name="title"></slot>
    </h1>
    <div class="buttons">
      <slot name="buttons"></slot>
    </div>
  </header>
</template>

<script>
export default {
  name: "TheHeader"
};
</script>

<style lang="scss" scoped>
.header {
  background: transparent;
  color: #4f4f4f;
  height: 90px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.title {
  font-size: 1.65rem;
  margin: 0;
  padding: 0;
  font-weight: normal;
}
</style>
