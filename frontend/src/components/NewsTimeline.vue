<template>
  <div>
    <div class="d-flex align-center justify-space-between mb-4">
      <h2 class="text-h5 font-weight-bold">{{ t('home.latest_news') }}</h2>
      <v-btn variant="text" color="primary" to="/nyheter" size="small">
        {{ t('home.see_all_news') }}
        <v-icon end>mdi-arrow-right</v-icon>
      </v-btn>
    </div>

    <v-timeline side="end" density="compact" truncate-line="both">
      <v-timeline-item
        v-for="post in posts"
        :key="post.id"
        :dot-color="post.post_type === 'message' ? 'accent' : 'primary'"
        size="small"
      >
        <v-card v-if="post.post_type === 'article'" :to="`/nyheter/${post.slug}`" class="cursor-pointer">
          <v-img v-if="post.image_url" :src="post.image_url" height="160" cover />
          <v-card-item>
            <v-card-title class="text-body-1 font-weight-bold">
              {{ lang === 'en' && post.title_en ? post.title_en : post.title_no }}
            </v-card-title>
            <v-card-subtitle>{{ formatDate(post.published_at || post.created_at) }}</v-card-subtitle>
          </v-card-item>
          <v-card-text v-if="post.excerpt_no" class="text-body-2">
            {{ lang === 'en' && post.excerpt_en ? post.excerpt_en : post.excerpt_no }}
          </v-card-text>
        </v-card>

        <div v-else class="pa-3">
          <p class="text-body-2 font-weight-medium mb-1">
            {{ lang === 'en' && post.content_en ? post.content_en : post.content_no }}
          </p>
          <p class="text-caption text-medium-emphasis">
            {{ formatDate(post.published_at || post.created_at) }}
          </p>
        </div>
      </v-timeline-item>
    </v-timeline>

    <div v-if="posts.length === 0" class="text-center py-8 text-medium-emphasis">
      {{ t('common.loading') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t, locale } = useI18n()
const lang = locale
const api = useApi()
const posts = ref<any[]>([])

onMounted(async () => {
  try {
    posts.value = await api.get('/news-timeline?limit=8')
  } catch {
    // API not available yet
  }
})

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('no-NO', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>
