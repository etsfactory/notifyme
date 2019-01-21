<template>
  <aside class="sidebar">
    <nav>
      <ul>
      <li v-for="(section, i) in sections" :key="i" class="links">
        <div @click="closeSidebar()">
          <router-link class="link" :to="section.url">{{ section.name }}</router-link>
        </div>
      </li>
      </ul>
    </nav>
  </aside>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "TheSidebar",
  props: {
    sections: {
      type: Array,
      required: true
    }
  },
  methods: {
    ...mapMutations(["setSidebarCollapsed"]),
    closeSidebar() {
      this.setSidebarCollapsed();
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
  margin-top: 2rem;
  margin: 2rem 0.5rem;
}
.link {
  color: white;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.2rem;
}
</style>
