import { createRouter, createWebHistory } from "vue-router";
import LogIn from "../components/LogIn.vue";
import HomePage from "../components/HomePage.vue";
import DashBoard from "../components/Dashboard.vue";
import Thresholds from "../components/Thresholds.vue";

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
    },
    {
        path: "/thresholds",
        name: "thresholds",
        component: Thresholds,
    }
]

const router = createRouter({
    history: createWebHistory(''), 
    routes,
  });

export default router;