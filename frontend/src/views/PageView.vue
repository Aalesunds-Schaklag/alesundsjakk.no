<template>
  <v-container class="py-12">
    <v-progress-linear v-if="loading" indeterminate color="primary" />

    <template v-if="page">
      <!-- Breadcrumb -->
      <v-breadcrumbs v-if="breadcrumbs.length > 1" :items="breadcrumbs" class="px-0 mb-4">
        <template #divider>
          <v-icon size="small">mdi-chevron-right</v-icon>
        </template>
      </v-breadcrumbs>

      <h1 class="text-h4 font-weight-bold mb-6">
        {{ lang === 'en' && page.title_en ? page.title_en : page.title_no }}
      </h1>

      <!-- Rich text content -->
      <div
        v-html="lang === 'en' && page.content_en ? page.content_en : page.content_no"
        class="text-body-1 wagtail-content"
      />

      <!-- Price table for PricingPage -->
      <div v-if="page.price_items?.length" class="mt-8">
        <h3 class="text-h6 font-weight-bold mb-4">
          {{ lang === 'en' ? 'Prices' : 'Priser' }}
        </h3>
        <v-table>
          <thead>
            <tr>
              <th>{{ lang === 'en' ? 'Category' : 'Kategori' }}</th>
              <th class="text-right">{{ lang === 'en' ? 'Price (NOK)' : 'Pris (NOK)' }}</th>
              <th>{{ lang === 'en' ? 'Description' : 'Beskrivelse' }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in page.price_items" :key="i">
              <td class="font-weight-medium">
                {{ lang === 'en' && item.category_en ? item.category_en : item.category_no }}
              </td>
              <td class="text-right">{{ item.price_nok }} kr</td>
              <td class="text-medium-emphasis">
                {{ lang === 'en' && item.description_en ? item.description_en : item.description_no }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </div>

      <!-- Sibling pages navigation -->
      <div v-if="siblings.length" class="mt-10">
        <v-divider class="mb-6" />
        <h3 class="text-h6 font-weight-bold mb-4">
          {{ lang === 'en' ? 'See also' : 'Se også' }}
        </h3>
        <v-row>
          <v-col v-for="sib in siblings" :key="sib.slug" cols="12" sm="6" md="4">
            <v-card
              :to="sib.url_path"
              variant="outlined"
              hover
            >
              <v-card-item>
                <v-card-title class="text-subtitle-1">
                  {{ lang === 'en' && sib.title_en ? sib.title_en : sib.title }}
                </v-card-title>
              </v-card-item>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </template>

    <!-- Not found -->
    <div v-if="!loading && !page" class="text-center py-12">
      <v-icon size="64" color="grey-lighten-1">mdi-file-question</v-icon>
      <h2 class="text-h5 mt-4 text-medium-emphasis">
        {{ lang === 'en' ? 'Page not found' : 'Siden ble ikke funnet' }}
      </h2>
      <v-btn to="/" color="primary" variant="tonal" class="mt-4">
        {{ lang === 'en' ? 'Go to homepage' : 'Gå til forsiden' }}
      </v-btn>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useWagtail, type WagtailPage, type NavItem } from '@/composables/useWagtail'
import { useAppStore } from '@/stores/app'

const { locale } = useI18n()
const lang = locale
const route = useRoute()
const { getPage, getPageByPath } = useWagtail()
const appStore = useAppStore()

const page = ref<WagtailPage | null>(null)
const loading = ref(true)

const pagePath = computed(() => {
  const match = route.params.pathMatch
  if (Array.isArray(match)) return '/' + match.join('/')
  if (match) return '/' + match
  // Fallback: use route.path
  return route.path
})

// Build breadcrumbs from the nav tree
const breadcrumbs = computed(() => {
  const crumbs: Array<{ title: string; to?: string; disabled?: boolean }> = [
    { title: locale.value === 'en' ? 'Home' : 'Hjem', to: '/' },
  ]

  const segments = pagePath.value.split('/').filter(Boolean)
  if (segments.length === 0) return crumbs

  // Walk the nav tree to find matching path
  let currentItems: NavItem[] = appStore.navTree
  let currentPath = ''

  for (let i = 0; i < segments.length; i++) {
    currentPath += '/' + segments[i]
    const found = currentItems.find(item => item.url_path === currentPath)
    if (found) {
      const isLast = i === segments.length - 1
      crumbs.push({
        title: locale.value === 'en' && found.title_en ? found.title_en : found.title,
        to: isLast ? undefined : found.url_path,
        disabled: isLast,
      })
      currentItems = found.children || []
    }
  }

  return crumbs
})

// Find sibling pages from nav tree
const siblings = computed(() => {
  const segments = pagePath.value.split('/').filter(Boolean)
  if (segments.length < 2) return [] // Only show siblings for nested pages

  const parentPath = '/' + segments.slice(0, -1).join('/')

  // Find parent in nav tree
  function findInTree(items: NavItem[], path: string): NavItem | null {
    for (const item of items) {
      if (item.url_path === path) return item
      const found = findInTree(item.children, path)
      if (found) return found
    }
    return null
  }

  const parent = findInTree(appStore.navTree, parentPath)
  if (!parent) return []

  // Return siblings excluding current page
  return parent.children.filter(c => c.url_path !== pagePath.value)
})

async function load() {
  loading.value = true
  page.value = null

  const path = pagePath.value
  const segments = path.split('/').filter(Boolean)

  if (segments.length === 1) {
    // Simple slug lookup
    page.value = await getPage(segments[0])
  } else {
    // Try path-based lookup first, then fall back to slug
    page.value = await getPageByPath(path)
    if (!page.value) {
      page.value = await getPage(segments[segments.length - 1])
    }
  }

  loading.value = false
}

onMounted(() => {
  appStore.loadNavigation()
  load()
})

watch(() => route.params.pathMatch, load)
watch(() => route.path, load)
</script>

<style scoped>
.wagtail-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

.wagtail-content :deep(th),
.wagtail-content :deep(td) {
  border: 1px solid rgba(0, 0, 0, 0.12);
  padding: 0.5rem 0.75rem;
  text-align: left;
}

.wagtail-content :deep(th) {
  background-color: rgba(0, 0, 0, 0.04);
  font-weight: 600;
}

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
