<template>
  <v-container class="py-12">
    <h1 class="text-h4 font-weight-bold mb-2">{{ t('schedule.title') }}</h1>
    <p class="text-subtitle-1 text-medium-emphasis mb-6">{{ t('schedule.subtitle') }}</p>

    <v-chip-group v-model="selectedCategory" mandatory class="mb-6">
      <v-chip v-for="cat in categories" :key="cat.value" :value="cat.value" filter>
        {{ t(cat.label) }}
      </v-chip>
    </v-chip-group>

    <v-card v-for="event in filteredEvents" :key="event.id" class="mb-3">
      <v-card-item>
        <template v-slot:prepend>
          <div class="text-center mr-4" style="min-width: 60px">
            <div class="text-h5 font-weight-bold text-primary">{{ dayOfMonth(event.start_date) }}</div>
            <div class="text-caption text-uppercase text-medium-emphasis">{{ monthShort(event.start_date) }}</div>
          </div>
        </template>
        <v-card-title class="text-body-1 font-weight-bold">
          {{ lang === 'en' && event.title_en ? event.title_en : event.title_no }}
        </v-card-title>
        <v-card-subtitle>
          <v-icon size="x-small" class="mr-1">mdi-clock</v-icon>
          {{ timeStr(event.start_date) }}
          <span v-if="event.end_date"> – {{ timeStr(event.end_date) }}</span>
          <v-chip v-if="event.category" size="x-small" class="ml-2" :color="categoryColor(event.category)">
            {{ event.category }}
          </v-chip>
        </v-card-subtitle>
      </v-card-item>
      <v-card-text v-if="event.location || event.description_no">
        <p v-if="event.location" class="text-body-2 mb-1">
          <v-icon size="small" class="mr-1">mdi-map-marker</v-icon>
          {{ event.location }}
        </p>
        <p v-if="event.description_no" class="text-body-2 text-medium-emphasis">
          {{ lang === 'en' && event.description_en ? event.description_en : event.description_no }}
        </p>
      </v-card-text>
      <v-card-actions v-if="event.spond_link">
        <v-btn v-if="event.spond_link" :href="event.spond_link" target="_blank" size="small" variant="text" color="primary">
          {{ t('schedule.spond') }}
          <v-icon end size="small">mdi-open-in-new</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-alert v-if="filteredEvents.length === 0" type="info" variant="tonal" class="mt-4">
      {{ t('schedule.no_events') }}
    </v-alert>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t, locale } = useI18n()
const lang = locale
const api = useApi()
const events = ref<any[]>([])
const selectedCategory = ref('all')

const categories = [
  { value: 'all', label: 'schedule.all' },
  { value: 'turnering', label: 'schedule.tournament' },
  { value: 'klubbkveld', label: 'schedule.club_evening' },
  { value: 'ungdom', label: 'schedule.youth' },
  { value: 'festival', label: 'schedule.festival' },
  { value: 'annet', label: 'schedule.other' },
]

const filteredEvents = computed(() => {
  if (selectedCategory.value === 'all') return events.value
  return events.value.filter((e: any) => e.category === selectedCategory.value)
})

onMounted(async () => {
  try {
    const data = await api.get<any>('/events?limit=100')
    events.value = data.items || []
  } catch { /* API not ready */ }
})

function categoryColor(cat: string) {
  const colors: Record<string, string> = {
    turnering: 'primary', klubbkveld: 'accent', ungdom: 'success', festival: 'secondary',
  }
  return colors[cat] || 'grey'
}

function dayOfMonth(iso: string) { return iso ? new Date(iso).getDate() : '' }
function monthShort(iso: string) { return iso ? new Date(iso).toLocaleDateString('no-NO', { month: 'short' }) : '' }
function timeStr(iso: string) { return iso ? new Date(iso).toLocaleTimeString('no-NO', { hour: '2-digit', minute: '2-digit' }) : '' }
</script>
