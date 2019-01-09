<template>
  <div id="app">
    <the-sidebar :sections="sections" :class="{ collapsed: sidebarCollapsed}"/>
    <div :class="{ content: true, collapsed: sidebarCollapsed}">
      <the-header/>
      <main class="main-content">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import TheHeader from "@/components/TheHeader.vue";
import TheSidebar from "@/components/TheSidebar.vue";
export default {
  name: "App",
  components: {
    TheHeader,
    TheSidebar
  },
  data: () => ({
    sections: [
      { name: "Users", url: "/users" },
      { name: "Bus filters", url: "/bus_filters" }
    ]
  }),
  computed: {
    ...mapState(["sidebarCollapsed"])
  }
};
</script>

<style lang="scss">
html,
body {
  color: #000;
  margin: 0;
  font-size: calc(15px + 0.4vmin);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
    "Ubuntu", "Helvetica Neue", Arial, sans-serif;
  width: 100%;
  height: 100%;
  background: #f3f3f3;
  line-height: 1.5em;
  font-weight: 400;
  font-style: normal;
}
#app {
  width: 100%;
  height: 100%;
  margin: 0;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.content {
  left: $sidebar-width;
  transition: left 0.3s cubic-bezier(0.2, 0.3, 0.25, 0.9);
  position: relative;
  position: fixed;
  width: 100%;
  &.collapsed {
    position: relative;
    left: 0;
  }
}
.main-content {
  padding: 1rem 3rem;
}
</style>
