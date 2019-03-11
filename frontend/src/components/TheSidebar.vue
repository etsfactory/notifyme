<template>
  <aside>
    <div class="logo">
      <logo/>
    </div>
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
}
.link {
  list-style: none;
  margin-top: 1rem;
  padding: 1rem 0;
  color: #bdbdbd;
  text-decoration: none;
  font-weight: bold;
  width: 100%;
  display: block;
  font-size: 1.2rem;
  transition: all 0.15s ease-in-out;
  &:hover {
    color: #4f4f4f;
    border-left: 7px solid $color-main;
  }
}
.router-link-active {
  color: #4f4f4f;
  border-left: 4px solid $color-main;
}
.link-container {
  width: 100%;
  padding: 0 2rem;
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
</style>
