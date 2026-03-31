<template>
  <div>
    <v-btn variant="text" color="primary" to="/admin/events" class="mb-4">
      <v-icon start>mdi-arrow-left</v-icon>
      {{ t('common.back') }}
    </v-btn>

    <h1 class="text-h5 font-weight-bold mb-6">
      {{ isNew ? t('admin.new_event') : t('admin.edit') }}
    </h1>

    <v-form @submit.prevent="save">
      <v-row>
        <v-col cols="12" md="8">
          <v-text-field v-model="form.title_no" label="Tittel (norsk)" required />
          <v-text-field v-model="form.title_en" label="Title (English)" />
          <v-textarea v-model="form.description_no" label="Beskrivelse (norsk)" rows="4" />
          <v-textarea v-model="form.description_en" label="Description (English)" rows="4" />
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            v-model="form.category"
            :items="['turnering', 'klubbkveld', 'ungdom', 'festival', 'annet']"
            label="Kategori"
          />
          <v-text-field v-model="form.location" label="Sted" />
          <v-text-field v-model="form.start_date" label="Startdato" type="datetime-local" required />
          <v-text-field v-model="form.end_date" label="Sluttdato" type="datetime-local" />
          <v-text-field v-model="form.spond_link" label="Spond-lenke" />
          <v-switch v-model="form.published" label="Publisert" color="success" />
          <v-btn type="submit" color="primary" block :loading="saving">
            {{ t('admin.save') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const api = useApi()
const saving = ref(false)

const isNew = computed(() => route.params.id === 'new')

const form = reactive({
  title_no: '',
  title_en: '',
  description_no: '',
  description_en: '',
  category: 'annet',
  location: '',
  start_date: '',
  end_date: '',
  spond_link: '',
  published: true,
})

onMounted(async () => {
  if (!isNew.value) {
    try {
      const events = await api.get<any[]>('/admin/events')
      const event = events.find((e: any) => e.id === route.params.id)
      if (event) Object.assign(form, event)
    } catch {}
  }
})

async function save() {
  saving.value = true
  try {
    if (isNew.value) {
      await api.post('/admin/events', form)
    } else {
      await api.put(`/admin/events/${route.params.id}`, form)
    }
    router.push('/admin/events')
  } catch {}
  saving.value = false
}
</script>
