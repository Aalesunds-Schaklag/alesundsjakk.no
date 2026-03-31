<template>
  <v-app-bar color="primary" density="compact">
    <v-app-bar-nav-icon @click="drawer = !drawer" />
    <v-toolbar-title>
      <router-link to="/" class="text-white text-decoration-none">
        Aalesunds Schaklag
      </router-link>
      <v-chip class="ml-2" size="small" color="secondary">Admin</v-chip>
    </v-toolbar-title>
    <template v-slot:append>
      <v-btn icon="mdi-logout" @click="logout" />
    </template>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" permanent>
    <v-list nav density="compact">
      <v-list-item
        v-for="item in adminNav"
        :key="item.to"
        :to="item.external ? undefined : item.to"
        :href="item.external ? item.to : undefined"
        :target="item.external ? '_blank' : undefined"
        :title="t(item.label)"
        :prepend-icon="item.icon"
        :append-icon="item.external ? 'mdi-open-in-new' : undefined"
      />
    </v-list>
  </v-navigation-drawer>

  <v-main>
    <v-container>
      <router-view />
    </v-container>
  </v-main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const router = useRouter()
const authStore = useAuthStore()
const drawer = ref(true)

const adminNav = [
  { to: '/admin', label: 'admin.dashboard', icon: 'mdi-view-dashboard' },
  { to: '/admin/posts', label: 'admin.posts', icon: 'mdi-newspaper' },
  { to: '/admin/events', label: 'admin.events', icon: 'mdi-calendar' },
  { to: '/cms/', label: 'admin.pages', icon: 'mdi-file-document', external: true },
  { to: '/admin/sponsors', label: 'admin.sponsors', icon: 'mdi-handshake' },
  { to: '/admin/media', label: 'admin.media', icon: 'mdi-image-multiple' },
]

function logout() {
  authStore.logout()
  router.push('/')
}
</script>
