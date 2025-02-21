import { createRouter, createWebHistory } from "vue-router";
import LogIn from "../components/LogIn.vue";
import HomePage from "../components/HomePage.vue";
import DashBoard from "../components/Dashboard.vue";
import Thresholds from "../components/Thresholds.vue";
import ManageDevices from "../components/ManageDevices.vue";

const routes = [
    {
        path: "/",
        name: "login",
        component: LogIn,
    },
    {
        path: "/homepage",
        name: "homepage",
        component: HomePage,
    },
    {
        path: "/dashboard",
        name: "dashboard",
        component: DashBoard,
        meta: { requiresAuth: true },
    },
    {
        path: "/thresholds",
        name: "thresholds",
        component: Thresholds,
    },
    {
      path: "/managedevices",
      name: "managedevices",
      component: ManageDevices,

    }
]

const router = createRouter({
    history: createWebHistory(''), 
    routes,
  });

  router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('user'); // Check if user data exists in localStorage
  
    if (to.meta.requiresAuth && !isAuthenticated) {
      // Redirect to login page if not authenticated
      next('/');
    } else {
      // Proceed to the requested route
      next();
    }
  });
export default router;