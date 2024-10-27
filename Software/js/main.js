const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes: [
    { path: '/', component: Login },
    { path: '/home', component: Home },
    { path: '/dashboard', component: Dashboard },
    { path: '/thresholds', component: Thresholds }
  ]
});

const app = Vue.createApp();

app.component('login', Login);
app.component('home', Home);
app.component('dashboard', Dashboard);
app.component('thresholds', Thresholds);

const vuetify = Vuetify.createVuetify()
app.use(vuetify)
app.use(router)
app.mount('#app')