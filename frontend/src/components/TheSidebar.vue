<template>
  <aside class="sidebar">
    <nav>
      <a href="#" class="link">Item1</a>
      <a href="#" class="link">Item2</a>
      <a href="#" class="link">Item3</a>
    </nav>
  </aside>
</template>

<script>

export default {
  name: 'TheSidebar',
};
</script>

<style lang="scss" scoped>

.sidebar {
  position: fixed;
  color: white;
  display: block;
  width: $sidebar-width;
  height: 100%;
  background: $sidebar-color;
  left: 0;
  top: 0;
  bottom: 0;
  transition: left 0.3s cubic-bezier(0.2, 0.3, 0.25, 0.9);
  overflow-x: hidden;
  &.collapsed {
    left: - $sidebar-width;
  }
}
.link {
  color: white;
}
</style>
