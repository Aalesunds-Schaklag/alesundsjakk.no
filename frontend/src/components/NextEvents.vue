<template>
  <div>
    <div class="d-flex align-center justify-space-between mb-4">
      <h2 class="text-h5 font-weight-bold">{{ t('home.next_events') }}</h2>
      <v-btn variant="text" color="primary" to="/terminliste" size="small">
        {{ t('home.see_schedule') }}
        <v-icon end>mdi-arrow-right</v-icon>
      </v-btn>
    </div>

    <v-row>
      <v-col v-for="event in events" :key="event.id" cols="12" md="4">
        <v-card class="h-100">
          <v-card-item>
            <template v-slot:prepend>
              <v-avatar :color="categoryColor(event.category)" size="48">
                <v-icon color="white">{{ categoryIcon(event.category) }}</v-icon>
              </v-avatar>
            </template>
            <v-card-title class="text-body-1 font-weight-bold">
              {{ lang === 'en' && event.title_en ? event.title_en : event.title_no }}
            </v-card-title>
            <v-card-subtitle>
              <v-icon size="small" class="mr-1">mdi-calendar</v-icon>
              {{ formatDate(event.start_date) }}
            </v-card-subtitle>
          </v-card-item>
          <v-card-text v-if="event.location">
            <v-icon size="small" class="mr-1">mdi-map-marker</v-icon>
            {{ event.location }}
          </v-card-text>
          <v-card-actions v-if="event.spond_link">
            <v-btn size="small" variant="text" :href="event.spond_link" target="_blank">
              Spond
              <v-icon end size="small">mdi-open-in-new</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="events.length === 0">
      <v-col>
        <v-alert type="info" variant="tonal">{{ t('schedule.no_events') }}</v-alert>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t, locale } = useI18n()
const lang = locale
const api = useApi()
const events = ref<any[]>([])

onMounted(async () => {
  try {
    events.value = await api.get('/events/next?count=3')
  } catch {
    // API not available yet — show empty
  }
})

function categoryColor(cat: string) {
  const colors: Record<string, string> = {
    turnering: '#1B2A4A',
    klubbkveld: '#2196F3',
    ungdom: '#4CAF50',
    festival: '#C9A84C',
  }
  return colors[cat] || '#757575'
}

function categoryIcon(cat: string) {
  const icons: Record<string, string> = {
    turnering: 'mdi-trophy',
    klubbkveld: 'mdi-chess-knight',
    ungdom: 'mdi-account-group',
    festival: 'mdi-party-popper',
  }
  return icons[cat] || 'mdi-calendar'
}

function formatDate(iso: string) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('no-NO', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
