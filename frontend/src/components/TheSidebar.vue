<template>
  <aside class="sidebar">
    <nav>
      <ul v-for="(section, i) in sections" :key="i" class="links">
        <li><router-link class="link" :to="section.url">{{ section.name }}</router-link></li>
      </ul>
    </nav>
  </aside>
</template>

<script>
export default {
  name: "TheSidebar",
  props: {
    sections: {
      type: Array,
      required: true
    }
  }
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
    left: -$sidebar-width;
  }
}
.links {
  list-style: none;
}
.link {
  color: white;
}
</style>
