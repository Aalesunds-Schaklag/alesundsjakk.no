import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useWagtail, type NavItem } from '@/composables/useWagtail'

const NAV_CACHE_KEY = 'nav_tree'
const NAV_CACHE_TTL = 5 * 60 * 1000 // 5 minutes

export const useAppStore = defineStore('app', () => {
  const locale = ref<string>(localStorage.getItem('locale') || 'no')
  const drawerOpen = ref(false)
  const navTree = ref<NavItem[]>([])
  const navLoaded = ref(false)

  function setLocale(l: string) {
    locale.value = l
    localStorage.setItem('locale', l)
  }

  function toggleDrawer() {
    drawerOpen.value = !drawerOpen.value
  }

  async function loadNavigation() {
    if (navLoaded.value) return

    // Try cached nav for instant render
    try {
      const cached = localStorage.getItem(NAV_CACHE_KEY)
      if (cached) {
        const { items, timestamp } = JSON.parse(cached)
        if (Date.now() - timestamp < NAV_CACHE_TTL) {
          navTree.value = items
        }
      }
    } catch { /* ignore cache errors */ }

    // Fetch fresh nav
    const { getNavigation } = useWagtail()
    const items = await getNavigation()
    if (items.length) {
      navTree.value = items
      navLoaded.value = true
      localStorage.setItem(NAV_CACHE_KEY, JSON.stringify({
        items,
        timestamp: Date.now(),
      }))
    } else if (navTree.value.length) {
      // Keep cached data if fetch failed
      navLoaded.value = true
    }
  }

  return { locale, drawerOpen, navTree, navLoaded, setLocale, toggleDrawer, loadNavigation }
})
