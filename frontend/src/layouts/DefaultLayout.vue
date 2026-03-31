<template>
  <v-app-bar color="primary" density="comfortable" elevation="2">
    <v-app-bar-nav-icon
      class="d-lg-none"
      @click="appStore.toggleDrawer()"
    />

    <v-toolbar-title class="d-flex align-center cursor-pointer" @click="router.push('/')">
      <img src="/logo.jpg" alt="Aalesunds Schaklag" height="40" class="mr-3 rounded" />
      <span class="text-subtitle-1 font-weight-bold d-none d-sm-block">Sjakk i Ålesund</span>
    </v-toolbar-title>

    <template v-slot:append>
      <div class="d-none d-lg-flex align-center ga-1">
        <v-btn
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          variant="text"
          size="small"
        >
          {{ t(item.label) }}
        </v-btn>
      </div>

      <LanguageSwitcher />

      <v-btn
        v-if="authStore.isLoggedIn"
        icon="mdi-cog"
        size="small"
        to="/admin"
      />
    </template>
  </v-app-bar>

  <v-navigation-drawer
    v-model="appStore.drawerOpen"
    temporary
  >
    <v-list nav>
      <v-list-item
        v-for="item in allNavItems"
        :key="item.to"
        :to="item.to"
        :title="t(item.label)"
        :prepend-icon="item.icon"
        @click="appStore.drawerOpen = false"
      />
    </v-list>
  </v-navigation-drawer>

  <v-main>
    <router-view />
    <AppFooter />
  </v-main>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import AppFooter from '@/components/AppFooter.vue'

const { t } = useI18n()
const router = useRouter()
const appStore = useAppStore()
const authStore = useAuthStore()

const navItems = [
  { to: '/bli-med', label: 'nav.join', icon: 'mdi-account-plus' },
  { to: '/terminliste', label: 'nav.schedule', icon: 'mdi-calendar' },
  { to: '/resultater', label: 'nav.results', icon: 'mdi-trophy' },
  { to: '/festival', label: 'nav.festival', icon: 'mdi-party-popper' },
  { to: '/lokaler', label: 'nav.rental', icon: 'mdi-home-city' },
  { to: '/om-oss', label: 'nav.about', icon: 'mdi-information' },
  { to: '/kontakt', label: 'nav.contact', icon: 'mdi-email' },
]

const allNavItems = [
  { to: '/', label: 'nav.home', icon: 'mdi-home' },
  ...navItems,
  { to: '/nyheter', label: 'nav.news', icon: 'mdi-newspaper' },
  { to: '/oppgave', label: 'nav.puzzle', icon: 'mdi-puzzle' },
]
</script>
