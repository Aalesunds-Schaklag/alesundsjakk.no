import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const alesundTheme = {
  dark: false,
  colors: {
    primary: '#1B2A4A',
    secondary: '#C9A84C',
    accent: '#2196F3',
    background: '#F5F5F0',
    surface: '#FFFFFF',
    error: '#D32F2F',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FF9800',
    'on-primary': '#FFFFFF',
    'on-secondary': '#1B2A4A',
    'on-background': '#212121',
    'on-surface': '#212121',
  },
}

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'alesundTheme',
    themes: {
      alesundTheme,
    },
  },
  defaults: {
    VCard: {
      elevation: 1,
    },
    VBtn: {
      rounded: 'lg',
    },
  },
})
