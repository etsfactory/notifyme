<template>
  <aside>
    <div class="logo">
      <router-link to="/">
        <logo/>
      </router-link>
    </div>
    <nav>
      <ul class="link-list">
        <li v-for="(section, i) in sections" :key="i">
          <router-link class="link" :to="section.url">
            <div class="border"></div>
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
import Logo from "@/components/Logo";

export default {
  name: "TheSidebar",
  components: {
    Logo
  },
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
.link-list {
  padding: 0;
  margin-top: 5rem;
  list-style: none;
  .router-link-active {
    color: #4f4f4f;
    .border {
      width: 4px;
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
  font-size: 1.2rem;
  transition: all 0.15s ease-in-out;
  letter-spacing: 0.15px;
  &:not(.router-link-active) {
    &:hover > .border {
      width: 7px;
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
  margin-right: 1rem;
}
.logo {
  width: 100%;
  text-align: center;
  margin-top: 3rem;
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
