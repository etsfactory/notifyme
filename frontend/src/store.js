import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    sidebarCollapsed: true
  },
  mutations: {
    setSidebarCollapsed(state) {
      state.sidebarCollapsed = !state.sidebarCollapsed
    }
  },
  actions: {}
});
