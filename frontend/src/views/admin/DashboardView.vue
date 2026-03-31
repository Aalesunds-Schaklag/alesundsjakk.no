<template>
  <div>
    <h1 class="text-h5 font-weight-bold mb-6">{{ t('admin.dashboard') }}</h1>

    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" variant="tonal">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon size="large">mdi-newspaper</v-icon>
            </template>
            <v-card-title class="text-h4">{{ stats.posts }}</v-card-title>
            <v-card-subtitle>{{ t('admin.posts') }}</v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="secondary" variant="tonal">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon size="large">mdi-calendar</v-icon>
            </template>
            <v-card-title class="text-h4">{{ stats.events }}</v-card-title>
            <v-card-subtitle>{{ t('admin.events') }}</v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" variant="tonal" href="/cms/" target="_blank">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon size="large">mdi-file-document</v-icon>
            </template>
            <v-card-title class="text-h6">Wagtail CMS</v-card-title>
            <v-card-subtitle>{{ t('admin.pages') }}</v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" variant="tonal">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon size="large">mdi-image-multiple</v-icon>
            </template>
            <v-card-title class="text-h4">{{ stats.media }}</v-card-title>
            <v-card-subtitle>{{ t('admin.media') }}</v-card-subtitle>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-item>
            <v-card-title>Hurtighandlinger</v-card-title>
          </v-card-item>
          <v-card-text>
            <v-btn color="primary" class="mr-2 mb-2" to="/admin/posts/new">
              <v-icon start>mdi-plus</v-icon>
              {{ t('admin.new_post') }}
            </v-btn>
            <v-btn color="secondary" class="mr-2 mb-2" to="/admin/events/new">
              <v-icon start>mdi-plus</v-icon>
              {{ t('admin.new_event') }}
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const api = useApi()
const stats = ref({ posts: 0, events: 0, pages: 0, media: 0 })

onMounted(async () => {
  try {
    const [posts, events, media] = await Promise.all([
      api.get<any[]>('/admin/posts'),
      api.get<any[]>('/admin/events'),
      api.get<any[]>('/media'),
    ])
    stats.value = {
      posts: posts.length,
      events: events.length,
      pages: 0,
      media: media.length,
    }
  } catch {}
})
</script>
