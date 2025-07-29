import { createApp } from 'vue'
import { Quasar } from 'quasar'
import { createPinia } from 'pinia'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/material-symbols-outlined/material-symbols-outlined.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

// Assumes your root component is App.vue
// and placed in same folder as main.js
import App from './App.vue'
import IndexPage from './pages/IndexPage.vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import MainLayout from './layouts/MainLayout.vue'

const pinia = createPinia();
const app = createApp(App)

const routes = [
    { path: '/', component: MainLayout, children: [{ path: '/', component: IndexPage }] },
];

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

app.use(Quasar, {
    plugins: {}, // import Quasar plugins and add here
});

app.use(pinia);
app.use(router);

// Assumes you have a <div id="app"></div> in your index.html
app.mount('#app');