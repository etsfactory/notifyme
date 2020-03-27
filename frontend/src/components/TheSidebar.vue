<template>
  <aside>
    <div class="logo">
      <router-link to="/">
        <logo/>
      </router-link>
    </div>
    <nav>
      <ul class="link-list">
        <li>
          <router-link class="link" to="/users">
            <div class="border"></div>
            <div class="link-container">
              <img svg-inline class="icon" src="../assets/icons/users.svg">
              Users
            </div>
          </router-link>
        </li>

        <li>
          <router-link class="link" to="/bus_filters">
            <div class="border"></div>
            <div class="link-container">
              <img svg-inline class="icon" src="../assets/icons/filter.svg">
              Bus filters
            </div>
          </router-link>
        </li>

        <li>
          <router-link class="link" to="/templates">
            <div class="border"></div>
            <div class="link-container">
              <img svg-inline class="icon" src="../assets/icons/templates.svg">
              Templates
            </div>
          </router-link>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script>
import { mapMutations } from "vuex";
import Logo from "@/components/Logo";

export default {
  name: "TheSidebar",
  components: {
    Logo
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
.link-list {
  padding: 0;
  margin-top: 5rem;
  list-style: none;
  .router-link-active {
    color: #4f4f4f;
    .border {
      width: 4px;
    }
    .icon path {
      fill: $color-main !important;
    }
  }
}
.link {
  position: relative;
  list-style: none;
  margin-top: 2rem;
  padding: 1rem 0;
  color: #bdbdbd;
  text-decoration: none;
  text-transform: uppercase;
  width: 100%;
  display: block;
  font-size: 1.1rem;
  transition: all 0.15s ease-in-out;
  letter-spacing: 0.15px;
  &:not(.router-link-active) {
    &:hover > .border {
      width: 7px;
    }
    &:hover .link-container .icon path {
      fill: $color-main !important;
    }
    &:hover {
      color: #4f4f4f;
    }
  }
}
.link-container {
  width: 100%;
  padding: 0 1.5rem;
}
.icon {
  margin-right: 0.5rem;
}
.logo {
  width: 100%;
  text-align: center;
  margin-top: 40px;
  svg {
    width: 70%;
    height: auto;
  }
}
.border {
  position: absolute;
  width: 0px;
  height: 97%;
  top: 0;
  left: 0;
  background: $color-degree;
  transition: width 0.15s ease-in-out;
  border-radius: 15px;
}
</style>
