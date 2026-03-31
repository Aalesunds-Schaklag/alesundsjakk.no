<template>
  <v-container class="py-12">
    <h1 class="text-h4 font-weight-bold mb-6">{{ t('nav.news') }}</h1>

    <v-row>
      <v-col v-for="post in posts" :key="post.id" cols="12" md="6" lg="4">
        <v-card :to="`/nyheter/${post.slug}`" class="h-100">
          <v-img v-if="post.image_url" :src="post.image_url" height="180" cover />
          <v-card-item>
            <v-card-title class="text-body-1 font-weight-bold">
              {{ lang === 'en' && post.title_en ? post.title_en : post.title_no }}
            </v-card-title>
            <v-card-subtitle>
              {{ formatDate(post.published_at || post.created_at) }}
              <v-chip v-if="post.category" size="x-small" class="ml-1">{{ post.category }}</v-chip>
            </v-card-subtitle>
          </v-card-item>
          <v-card-text v-if="post.excerpt_no" class="text-body-2">
            {{ lang === 'en' && post.excerpt_en ? post.excerpt_en : post.excerpt_no }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <div v-if="posts.length === 0" class="text-center py-12 text-medium-emphasis">
      {{ t('common.loading') }}
    </div>
  </v-container>
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
    const data = await api.get<any>('/posts?post_type=article')
    posts.value = data.items || []
  } catch {}
})

function formatDate(iso: string) {
  return iso ? new Date(iso).toLocaleDateString('no-NO', { day: 'numeric', month: 'long', year: 'numeric' }) : ''
}
</script>
