<template>
  <v-sheet v-if="sponsors.length" color="background" class="py-8">
    <v-container>
      <h3 class="text-h6 text-center text-medium-emphasis mb-6">{{ t('home.sponsors') }}</h3>
      <v-row justify="center" align="center">
        <v-col
          v-for="sponsor in sponsors"
          :key="sponsor.id"
          cols="auto"
          class="text-center"
        >
          <a v-if="sponsor.website_url" :href="sponsor.website_url" target="_blank">
            <v-img
              v-if="sponsor.logo_url"
              :src="sponsor.logo_url"
              :alt="sponsor.name"
              height="48"
              width="160"
              contain
              class="mx-4"
            />
            <span v-else class="text-body-2 font-weight-bold text-medium-emphasis">{{ sponsor.name }}</span>
          </a>
          <span v-else class="text-body-2 font-weight-bold text-medium-emphasis">{{ sponsor.name }}</span>
        </v-col>
      </v-row>
    </v-container>
  </v-sheet>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const api = useApi()
const sponsors = ref<any[]>([])

onMounted(async () => {
  try {
    sponsors.value = await api.get('/sponsors?scope=global')
  } catch {
    // API not available
  }
})
</script>
