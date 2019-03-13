<template>
  <div id="app">
    <div class="grid">
      <div class="sidebar">
        <the-sidebar :sections="sections"/>
      </div>
      <div class="content">
        <main class="main-content">
          <router-view></router-view>
        </main>
      </div>
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
      { name: "Users", url: "/users", icon: "fas fa-users" },
      { name: "Bus filters", url: "/bus_filters", icon: "fas fa-filter" },
      { name: "Templates", url: "/templates", icon: "fas fa-envelope" }
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
  font-size: calc(11px + 0.2vmax);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
    "Ubuntu", "Helvetica Neue", Arial, sans-serif;
  width: 100%;
  height: 100%;
  background: #fdfdfd;
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
.grid {
  display: flex;
}
.sidebar {
  width: $sidebar-width;
}
.content {
  transition: left 0.3s cubic-bezier(0.2, 0.3, 0.25, 0.9);
  position: relative;
  padding: 0 3rem;
  width: 90%;
  &.collapsed {
    position: relative;
    left: 0;
  }
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
a,
a:active,
a:focus,
button {
  outline: none;
}
.center {
  margin: 0px auto;
  text-align: center;
}
.warning {
  padding: 1rem;
  margin: 1rem auto;
  background-color: #fff5e1;
}
.vue-form-generator * {
  box-sizing: border-box;
}
.vue-form-generator .form-control {
  display: block;
  padding: 6px 12px;
  font-size: 14px;
  line-height: 1.42857143;
  color: #555;
  background-color: #fff;
  background-image: none;
  border: 1px solid #ccc;
  border-radius: 4px;
  -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}
.vue-form-generator .form-control:not([class*=" col-"]) {
  width: 100%;
}
.form-group:not([class*=" col-"]) {
  width: 100%;
}
.vue-form-generator .field-wrap {
  display: flex;
}
.vue-form-generator .field-input .wrapper {
  width: 100%;
}
.form-group {
  display: inline-block;
  vertical-align: top;
  margin-bottom: 1rem;
}
.create-icon {
  cursor: pointer;
  margin-right: 0.7rem;
  color: $color-main;
}
.button-main,
.field-wrap input[type="submit"] {
  padding: 0.6rem 1rem !important;
  background: #f2f2f2;
  border: none !important;
  cursor: pointer;
  font-weight: bold !important;
  color: #333333;
  margin: 0px auto;
  border-radius: 3px;
  text-transform: uppercase;
  display: flex;
  align-items: center;
}
.field-wrap input[type="submit"],
.button-submit {
  padding: 0.8rem 2rem !important;
  margin-top: 2rem;
}
.button-grey {
  padding: 0.8rem 3rem !important;
  background: #888888;
  border: none !important;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold !important;
  color: white;
  margin: 0px auto;
}
.modal-bg {
  width: 100vw;
  min-height: 100vh;
  height: 100%;
  position: absolute;
  bottom: 0;
  right: 0;
  top: 0;
  background-color: rgba(26, 48, 54, 0.85);
  z-index: 1;
}
.modal {
  position: fixed;
  width: 100vw;
  min-height: 100vh;
  height: 100%;
  bottom: 0;
  right: 0;
  top: 0;
  z-index: 2;
  visibility: hidden;
  opacity: 0;
  overflow: hiden;
  visibility: visible;
  opacity: 1;

  &-inner {
    position: relative;
    margin: 5% auto;
    display: flex;
    align-items: center;
    flex-direction: column;
    max-width: 800px;
    width: 500px;
    background-color: #fff;
    border-radius: 6px;
    z-index: 3;
    padding: 4rem 2rem;
  }
}
.modal-title {
  font-size: 3rem;
  font-weight: bold;
}
.modal-subtitle {
  text-align: center;
  margin-bottom: 4rem;
}
.modal-close {
  position: absolute;
  right: 1rem;
  top: 0.5rem;
  width: 2rem;
  height: 2rem;
  font-size: 1.5rem;
  font-weight: 300;
  border-radius: 100%;
  z-index: 4;
  color: black;
  line-height: 3rem;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
}
.modal-hide {
  visibility: hidden !important;
  opacity: 0 !important;
}
.modal-buttons-container {
  position: absolute;
  bottom: 0;
  left: 0;
  display: flex;
  width: 100%;
}
.modal-button {
  width: 50%;
  padding: 1.4rem 0;
  border: none;
  cursor: pointer;
  font-weight: bold;
}
.modal-accept {
  background: #fc7169;
  color: white;
  &:hover {
    background: #e7645d;
  }
}
.modal-exit {
  background: #b6bece;
  color: white;
  &:hover {
    background: #a0aabe;
  }
}
pre,
code {
  font-family: monospace, monospace;
}
pre {
  overflow: auto;
}
pre > code {
  display: block;
  padding: 1rem;
  word-wrap: normal;
}
.hljs {
  background: transparent;
}
@media (max-width: 1250px) {
  .grid {
    flex-wrap: wrap;
  }
  .sidebar {
    width: 100%;
    min-width: 100%;
    .logo {
      width: 20%;
      margin-top: 1rem;
    }
    aside {
      display: flex;
      align-items: center;
      nav {
        width: 80%;
        min-width: 80%;
        .link-list {
          display: flex;
          align-items: center;
          width: 100%;
          min-width: 100%;
          margin-top: 0;
          justify-content: space-evenly;
          .link-container {
            padding: 0 1rem;
          }
        }
      }
    }
  }
  .content {
    min-width: 100%;
    width: 100%;
    margin-top: 2rem;
  }
}
</style>
