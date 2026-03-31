<template>
  <div>
    <h1 class="text-h5 font-weight-bold mb-6">{{ t('admin.sponsors') }}</h1>

    <v-dialog v-model="dialog" max-width="500">
      <template v-slot:activator="{ props }">
        <v-btn color="primary" v-bind="props" class="mb-4">
          <v-icon start>mdi-plus</v-icon>
          Ny sponsor
        </v-btn>
      </template>
      <v-card>
        <v-card-title>{{ editing ? 'Rediger sponsor' : 'Ny sponsor' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.name" label="Navn" required />
          <v-text-field v-model="form.logo_url" label="Logo-URL" />
          <v-text-field v-model="form.website_url" label="Nettside" />
          <v-select v-model="form.tier" :items="['hovedsponsor', 'sponsor', 'stotter']" label="Nivå" />
          <v-select v-model="form.scope" :items="['global', 'festival']" label="Omfang" />
          <v-text-field v-model.number="form.sort_order" label="Sortering" type="number" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false">Avbryt</v-btn>
          <v-btn color="primary" @click="saveSponsor">{{ t('admin.save') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-table>
      <thead>
        <tr>
          <th>Navn</th>
          <th>Nivå</th>
          <th>Omfang</th>
          <th>Aktiv</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in sponsors" :key="s.id">
          <td>{{ s.name }}</td>
          <td><v-chip size="x-small">{{ s.tier }}</v-chip></td>
          <td>{{ s.scope }}</td>
          <td><v-icon :color="s.is_active ? 'success' : 'grey'">{{ s.is_active ? 'mdi-check' : 'mdi-close' }}</v-icon></td>
          <td>
            <v-btn icon="mdi-pencil" size="small" variant="text" @click="edit(s)" />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const api = useApi()
const sponsors = ref<any[]>([])
const dialog = ref(false)
const editing = ref<string | null>(null)
const form = reactive({ name: '', logo_url: '', website_url: '', tier: 'sponsor', scope: 'global', sort_order: 0 })

onMounted(load)

async function load() {
  try { sponsors.value = await api.get('/admin/sponsors') } catch {}
}

function edit(s: any) {
  editing.value = s.id
  Object.assign(form, s)
  dialog.value = true
}

async function saveSponsor() {
  if (editing.value) {
    await api.put(`/admin/sponsors/${editing.value}`, form)
  } else {
    await api.post('/admin/sponsors', form)
  }
  dialog.value = false
  editing.value = null
  await load()
}
</script>
