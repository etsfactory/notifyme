<template>
  <header class="header">
    <nav class="link-list">
      <ul class="menu">
        <li>
          <router-link class="logo" to="/">
            <h1 class="title">Notify.me</h1>
          </router-link>
        </li>
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
  </header>
</template>

<script>
import { mapMutations } from "vuex";
export default {
  name: "TheHeader",
  props: {
    sections: Array
  }
};
</script>

<style lang="scss" scoped>
.header {
  background: linear-gradient(to right, $color-main-dark, $color-secondary);
  color: white;
  height: 50px;
  position: relative;
}
.title {
  margin-left: 1rem;
  display: inline;
  font-size: 1.4rem;
}
.logo {
  color: white;
}
.link-list {
  height: 100%;
}
.menu {
  height: 100%;
  display: flex;
  margin: 0;
  padding: 0;
  margin-left: 40px;
  list-style: none;
  align-items: center;
  & :nth-child(2) {
    margin-left: 40px;
  }
}
.link {
  padding: 0 1.5rem;
  color: white;
  text-decoration: none;
  font-weight: bold;
  width: 100%;
  height: 100%;
  display: block;
  font-size: 1.2rem;
}
.icon {
  margin-right: 0.2rem;
}
</style>
