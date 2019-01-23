<template>
  <aside class="sidebar">
    <nav>
      <ul class="link-list">
        <li v-for="(section, i) in sections" :key="i">
          <router-link class="link" :to="section.url">
            <div class="link-container">
              <i class="icon" :class="section.icon"></i>
              {{ section.name }}
            </div>
          </router-link>
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
  background: linear-gradient(to bottom, $sidebar-color, $sidebar-color-dark);
  left: 0;
  top: 0;
  bottom: 0;
  transition: left 0.3s cubic-bezier(0.2, 0.3, 0.25, 0.9);
  overflow-x: hidden;
  &.collapsed {
    left: -$sidebar-width;
  }
}
.link-list {
  padding: 0;
  margin-top: 2.9rem;
}
.link {
  list-style: none;
  margin-top: 1rem;
  padding: 1rem 0;
  color: white;
  text-decoration: none;
  font-weight: bold;
  width: 100%;
  display: block;
  font-size: 1.2rem;
  &:hover {
    background: $color-main-dark;
  }
}
.link-container {
  display: flex;
  width: 90%;
  justify-content: center;
}
.icon {
  margin-right: 1rem;
}
</style>
