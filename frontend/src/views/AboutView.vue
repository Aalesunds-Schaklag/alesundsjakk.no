<template>
  <v-container class="py-12">
    <h1 class="text-h4 font-weight-bold mb-2">{{ t('about.title') }}</h1>

    <v-progress-linear v-if="!page && !loaded" indeterminate color="primary" class="mt-4" />

    <!-- Wagtail content -->
    <div v-if="page" v-html="lang === 'en' && page.content_en ? page.content_en : page.content_no" class="text-body-1 mt-6 wagtail-content" />

    <!-- Fallback if Wagtail unavailable -->
    <div v-else-if="loaded" class="mt-6">
      <v-card class="mb-6">
        <v-card-item>
          <template v-slot:prepend>
            <v-avatar color="primary" size="56">
              <img src="/logo.jpg" alt="Logo" />
            </v-avatar>
          </template>
          <v-card-title>{{ t('about.history') }}</v-card-title>
        </v-card-item>
        <v-card-text class="text-body-1">
          <p>
            Aalesunds Schaklag ble stiftet i 1913 og er en av de eldste sjakklubbene i Norge.
            Klubben holder til i egne lokaler på Steinvågvegen 60 på Aspøya i Ålesund.
          </p>
        </v-card-text>
      </v-card>
    </div>

    <!-- Child page links -->
    <div v-if="children.length" class="mt-8">
      <v-row>
        <v-col v-for="child in children" :key="child.slug" cols="12" sm="6" md="4">
          <v-card
            :to="child.url_path"
            variant="outlined"
            hover
            class="h-100"
          >
            <v-card-item>
              <template v-slot:prepend v-if="child.icon">
                <v-icon color="primary">{{ child.icon }}</v-icon>
              </template>
              <v-card-title class="text-subtitle-1">
                {{ lang === 'en' && child.title_en ? child.title_en : child.title }}
              </v-card-title>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWagtail } from '@/composables/useWagtail'
import { useAppStore } from '@/stores/app'
import type { NavItem } from '@/composables/useWagtail'

const { t, locale } = useI18n()
const lang = locale
const { getPage } = useWagtail()
const appStore = useAppStore()
const page = ref<any>(null)
const loaded = ref(false)

// Find children of "om-oss" from nav tree
const children = computed<NavItem[]>(() => {
  const omOss = appStore.navTree.find(item => item.slug === 'om-oss')
  return omOss?.children || []
})

onMounted(async () => {
  appStore.loadNavigation()
  page.value = await getPage('om-oss')
  loaded.value = true
})
</script>

<style scoped>
.wagtail-content :deep(h2) {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}
.wagtail-content :deep(h3) {
  margin-top: 1.25rem;
  margin-bottom: 0.5rem;
}
.wagtail-content :deep(ul) {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}
.wagtail-content :deep(p) {
  margin-bottom: 0.75rem;
}
</style>
