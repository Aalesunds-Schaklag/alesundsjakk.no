<template>
  <div>
    <div class="d-flex align-center justify-space-between mb-6">
      <h1 class="text-h5 font-weight-bold">{{ t('admin.events') }}</h1>
      <v-btn color="primary" to="/admin/events/new">
        <v-icon start>mdi-plus</v-icon>
        {{ t('admin.new_event') }}
      </v-btn>
    </div>

    <v-table>
      <thead>
        <tr>
          <th>Dato</th>
          <th>{{ t('admin.title') }}</th>
          <th>{{ t('admin.category') }}</th>
          <th>Sted</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="event in events" :key="event.id">
          <td class="text-caption">{{ event.start_date?.slice(0, 10) }}</td>
          <td>{{ event.title_no }}</td>
          <td><v-chip size="x-small">{{ event.category }}</v-chip></td>
          <td class="text-caption">{{ event.location || '-' }}</td>
          <td>
            <v-btn icon="mdi-pencil" size="small" variant="text" :to="`/admin/events/${event.id}`" />
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="deleteEvent(event.id)" />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const api = useApi()
const events = ref<any[]>([])

onMounted(load)

async function load() {
  try { events.value = await api.get('/admin/events') } catch {}
}

async function deleteEvent(id: string) {
  if (confirm('Er du sikker?')) {
    await api.del(`/admin/events/${id}`)
    await load()
  }
}
</script>
