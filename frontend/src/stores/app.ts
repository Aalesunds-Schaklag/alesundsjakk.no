import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const locale = ref<string>(localStorage.getItem('locale') || 'no')
  const drawerOpen = ref(false)

  function setLocale(l: string) {
    locale.value = l
    localStorage.setItem('locale', l)
  }

  function toggleDrawer() {
    drawerOpen.value = !drawerOpen.value
  }

  return { locale, drawerOpen, setLocale, toggleDrawer }
})
