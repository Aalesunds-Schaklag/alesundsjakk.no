<template>
  <div>
    <h1 class="text-h5 font-weight-bold mb-6">{{ t('admin.media') }}</h1>

    <v-file-input
      v-model="uploadFile"
      label="Last opp bilde"
      accept="image/*"
      prepend-icon="mdi-camera"
      class="mb-4"
      @update:model-value="upload"
    />

    <v-progress-linear v-if="uploading" indeterminate color="primary" class="mb-4" />

    <v-row>
      <v-col v-for="file in files" :key="file.id" cols="6" sm="4" md="3" lg="2">
        <v-card @click="copyUrl(file.url)">
          <v-img :src="file.url" height="120" cover />
          <v-card-text class="pa-2">
            <p class="text-caption text-truncate">{{ file.filename }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snack" :timeout="2000" color="success">
      URL kopiert!
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const api = useApi()
const files = ref<any[]>([])
const uploadFile = ref<File[] | null>(null)
const uploading = ref(false)
const snack = ref(false)

onMounted(load)

async function load() {
  try { files.value = await api.get('/media') } catch {}
}

async function upload() {
  if (!uploadFile.value?.length) return
  uploading.value = true
  try {
    await api.upload(uploadFile.value[0])
    await load()
  } catch {}
  uploading.value = false
  uploadFile.value = null
}

function copyUrl(url: string) {
  navigator.clipboard.writeText(window.location.origin + url)
  snack.value = true
}
</script>
