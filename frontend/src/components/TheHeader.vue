<template>
  <header class="header">
    <button class="button-toggle" @click="toggleSidebar()">&#9776;</button>
    <router-link class="logo" to="/"><h1 class="title">Notify.me</h1></router-link>
  </header>
</template>

<script>

import { mapMutations } from "vuex"
export default {
  name: 'TheHeader',
  methods: {
    ...mapMutations(['setSidebarCollapsed']),
    toggleSidebar() {
      this.setSidebarCollapsed();
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  background: $color-main-dark;
  color: white;
}
.button-toggle {
  min-width: 50px;
  min-height: 50px;
  color: white;
  background: transparent;
  border: none;
  font-size: 1.3rem;
  cursor: pointer;
  margin-left: 1rem;
  padding-top: 0.25rem;
  display: inline;
}
.title {
  margin-left: 1rem;
  display: inline;
  font-size: 1.4rem;
}
.logo {
  color: white;
}
</style>
