import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Users from "./views/Users.vue";
import User from "./views/User.vue";
import BusFilters from "./views/BusFilters.vue";
import BusFilter from "./views/BusFilter.vue";
import Templates from "./views/Templates.vue";
import Template from "./views/Template.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/users",
      name: "users",
      component: Users
    },
    {
      path: "/users/:id",
      name: "user",
      component: User
    },
    {
      path: "/bus_filters",
      name: "bus_filters",
      component: BusFilters
    },
    {
      path: "/bus_filters/:id",
      name: "bus_filter",
      component: BusFilter
    },
    {
      path: "/templates",
      name: "templates",
      component: Templates
    },
    {
      path: "/templates/:id",
      name: "template",
      component: Template
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue")
    }
  ]
});
