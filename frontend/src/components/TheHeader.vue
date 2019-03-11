<template>
  <header class="header">
    <nav class="link-list">
      <h1 class="title">
        <slot name="title"></slot>
      </h1>
      <div class="buttons">
        <slot name="buttons"></slot>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: "TheHeader",
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
}
.title {
  font-size: 1.65rem;
  margin: 0;
  padding: 0;
  font-weight: 600;
}
</style>
