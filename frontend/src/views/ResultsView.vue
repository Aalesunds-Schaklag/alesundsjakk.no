<template>
  <v-container class="py-12">
    <h1 class="text-h4 font-weight-bold mb-2">{{ t('results.title') }}</h1>
    <p class="text-subtitle-1 text-medium-emphasis mb-8">{{ t('results.subtitle') }}</p>

    <v-card v-for="event in tournaments" :key="event.id" class="mb-3">
      <v-card-item>
        <template v-slot:prepend>
          <v-icon color="secondary" size="large">mdi-trophy</v-icon>
        </template>
        <v-card-title class="text-body-1 font-weight-bold">
          {{ lang === 'en' && event.title_en ? event.title_en : event.title_no }}
        </v-card-title>
        <v-card-subtitle>{{ formatDate(event.start_date) }}</v-card-subtitle>
      </v-card-item>
    </v-card>

    <v-alert v-if="tournaments.length === 0" type="info" variant="tonal">
      {{ t('results.no_results') }}
    </v-alert>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t, locale } = useI18n()
const lang = locale
const api = useApi()
const tournaments = ref<any[]>([])

onMounted(async () => {
  try {
    const data = await api.get<any>('/events?category=turnering&upcoming=false&limit=20')
    tournaments.value = data.items || []
  } catch { /* API not ready */ }
})

function formatDate(iso: string) {
  return iso ? new Date(iso).toLocaleDateString('no-NO', { day: 'numeric', month: 'long', year: 'numeric' }) : ''
}
</script>
