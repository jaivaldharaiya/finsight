// src/plugins/vuetify.js

// Import styles and icon fonts
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Define your custom theme
const finsightTheme = {
  dark: false, // You can switch this to true for a dark mode
  colors: {
    background: '#F8F9FA', // A light grey background
    surface: '#FFFFFF', // The color of cards, sheets, etc.
    primary: '#1976D2', // A professional blue
    secondary: '#424242',
    accent: '#82B1FF',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50', // Green for success messages or positive trends
    warning: '#FB8C00',
  },
}

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'finsightTheme',
    themes: {
      finsightTheme,
    },
  },
  icons: {
    defaultSet: 'mdi', // This is already the default value - only for display purposes
  },
})