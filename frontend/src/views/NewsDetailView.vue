<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-btn variant="text" color="primary" to="/nyheter" class="mb-4">
          <v-icon start>mdi-arrow-left</v-icon>
          {{ t('common.back') }}
        </v-btn>

        <v-progress-linear v-if="loading" indeterminate color="primary" />

        <article v-if="post">
          <v-img v-if="post.image_url" :src="post.image_url" height="300" cover class="rounded-lg mb-6" />
          <h1 class="text-h4 font-weight-bold mb-2">
            {{ lang === 'en' && post.title_en ? post.title_en : post.title_no }}
          </h1>
          <p class="text-caption text-medium-emphasis mb-6">
            {{ formatDate(post.published_at || post.created_at) }}
            <v-chip v-if="post.category" size="x-small" class="ml-2">{{ post.category }}</v-chip>
          </p>
          <div v-html="lang === 'en' && post.content_en ? post.content_en : post.content_no" class="text-body-1" />
        </article>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t, locale } = useI18n()
const lang = locale
const route = useRoute()
const api = useApi()
const post = ref<any>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    post.value = await api.get(`/posts/${route.params.slug}`)
  } catch {}
  loading.value = false
})

function formatDate(iso: string) {
  return iso ? new Date(iso).toLocaleDateString('no-NO', { day: 'numeric', month: 'long', year: 'numeric' }) : ''
}
</script>
