// src/main.js

import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Correctly imports the router
import vuetify from './plugins/vuetify' // Correctly imports Vuetify config
import { loadFonts } from './plugins/webfontloader'

// Ensure you have run: npm install webfontloader
loadFonts()

const app = createApp(App)

// Use the plugins
app.use(vuetify)
app.use(router) // This is crucial for displaying pages

app.mount('#app')