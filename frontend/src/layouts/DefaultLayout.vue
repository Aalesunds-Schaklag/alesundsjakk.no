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
        <template v-for="item in navTree" :key="item.id">
          <!-- Item with children: dropdown menu -->
          <v-menu v-if="item.children.length" open-on-hover :close-on-content-click="true">
            <template #activator="{ props }">
              <v-btn v-bind="props" variant="text" size="small">
                {{ localizedTitle(item) }}
                <v-icon end size="x-small">mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <v-list density="compact">
              <v-list-item :to="resolveLink(item)">
                <v-list-item-title class="font-weight-bold">{{ localizedTitle(item) }}</v-list-item-title>
              </v-list-item>
              <v-divider />
              <v-list-item
                v-for="child in item.children"
                :key="child.id"
                :to="resolveLink(child)"
              >
                <v-list-item-title>{{ localizedTitle(child) }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <!-- Leaf item: simple button -->
          <v-btn v-else :to="resolveLink(item)" variant="text" size="small">
            {{ localizedTitle(item) }}
          </v-btn>
        </template>
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
      <!-- Home is always first -->
      <v-list-item
        to="/"
        :title="t('nav.home')"
        prepend-icon="mdi-home"
        @click="appStore.drawerOpen = false"
      />

      <template v-for="item in navTree" :key="item.id">
        <!-- Items with children: expandable group -->
        <v-list-group v-if="item.children.length">
          <template #activator="{ props }">
            <v-list-item
              v-bind="props"
              :prepend-icon="item.icon || undefined"
              :title="localizedTitle(item)"
            />
          </template>
          <v-list-item
            :to="resolveLink(item)"
            :title="localizedTitle(item)"
            prepend-icon="mdi-arrow-right"
            @click="appStore.drawerOpen = false"
          />
          <v-list-item
            v-for="child in item.children"
            :key="child.id"
            :to="resolveLink(child)"
            :title="localizedTitle(child)"
            :prepend-icon="child.icon || 'mdi-circle-small'"
            @click="appStore.drawerOpen = false"
          />
        </v-list-group>

        <!-- Leaf items -->
        <v-list-item
          v-else
          :to="resolveLink(item)"
          :title="localizedTitle(item)"
          :prepend-icon="item.icon || undefined"
          @click="appStore.drawerOpen = false"
        />
      </template>
    </v-list>
  </v-navigation-drawer>

  <v-main>
    <router-view />
    <AppFooter />
  </v-main>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import type { NavItem } from '@/composables/useWagtail'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import AppFooter from '@/components/AppFooter.vue'

const { t, locale } = useI18n()
const router = useRouter()
const appStore = useAppStore()
const authStore = useAuthStore()

const navTree = computed(() => appStore.navTree)

function localizedTitle(item: NavItem): string {
  if (locale.value === 'en' && item.title_en) return item.title_en
  return item.title
}

function resolveLink(item: NavItem): string | { name: string } {
  if (item.vue_route_name) return { name: item.vue_route_name }
  return item.url_path
}

onMounted(() => {
  appStore.loadNavigation()
})
</script>
