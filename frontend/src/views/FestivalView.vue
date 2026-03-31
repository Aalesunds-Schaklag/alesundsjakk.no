<template>
  <div>
    <v-sheet color="secondary" class="py-12 text-center">
      <v-container>
        <h1 class="text-h3 font-weight-bold text-primary mb-2">{{ t('festival.title') }}</h1>
        <p class="text-h6 text-primary" style="opacity: 0.8">{{ t('festival.subtitle') }}</p>
        <v-btn
          color="primary"
          size="large"
          class="mt-6"
          rounded="pill"
          href="#registration"
        >
          {{ t('festival.register_now') }}
        </v-btn>
      </v-container>
    </v-sheet>

    <v-container class="py-12">
      <v-row>
        <v-col cols="12" md="8">
          <div v-if="page" v-html="page.content_no" class="text-body-1 mb-8" />

          <div v-else>
            <h2 class="text-h5 font-weight-bold mb-4">{{ t('festival.program') }}</h2>
            <v-card class="mb-6">
              <v-card-text>
                <p class="text-body-1">
                  Ålesund Sjakkfestival er en årlig sjakkfestival arrangert av Aalesunds Schaklag.
                  Festivalen har turneringer for alle nivåer, fra nybegynnere til mesternivå.
                </p>
                <p class="text-body-1 mt-4">
                  Programmet og påmelding publiseres når festivalen nærmer seg.
                  Følg med på nettsiden og våre sosiale medier for oppdateringer.
                </p>
              </v-card-text>
            </v-card>

            <h2 class="text-h5 font-weight-bold mb-4" id="registration">{{ t('festival.registration') }}</h2>
            <v-card class="mb-6">
              <v-card-text>
                <p class="text-body-1">
                  Påmeldingslenke publiseres her når påmeldingen åpner.
                </p>
              </v-card-text>
            </v-card>

            <h2 class="text-h5 font-weight-bold mb-4">{{ t('festival.practical') }}</h2>
            <v-card>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item prepend-icon="mdi-map-marker">
                    <v-list-item-title>Aalesunds Schaklag</v-list-item-title>
                    <v-list-item-subtitle>Steinvågvegen 60, 6005 Ålesund</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item prepend-icon="mdi-phone">
                    <v-list-item-title>+47 932 58 938</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </div>
        </v-col>

        <v-col cols="12" md="4">
          <v-card class="mb-6" color="primary" variant="tonal">
            <v-card-item>
              <v-card-title>{{ t('festival.guests') }}</v-card-title>
            </v-card-item>
            <v-card-text class="text-body-2">
              Informasjon om spesielle gjester publiseres når det er bekreftet.
            </v-card-text>
          </v-card>

          <v-card>
            <v-card-item>
              <v-card-title>{{ t('festival.sponsors') }}</v-card-title>
            </v-card-item>
            <v-card-text>
              <div v-for="s in sponsors" :key="s.id" class="mb-2">
                <a v-if="s.website_url" :href="s.website_url" target="_blank" class="font-weight-bold">
                  {{ s.name }}
                </a>
                <span v-else class="font-weight-bold">{{ s.name }}</span>
                <v-chip size="x-small" class="ml-1">{{ s.tier }}</v-chip>
              </div>
              <p v-if="!sponsors.length" class="text-body-2 text-medium-emphasis">
                Sponsorinformasjon kommer.
              </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'
import { useWagtail } from '@/composables/useWagtail'

const { t } = useI18n()
const api = useApi()
const { getPage } = useWagtail()
const page = ref<any>(null)
const sponsors = ref<any[]>([])

onMounted(async () => {
  page.value = await getPage('festival')
  try { sponsors.value = await api.get('/sponsors?scope=festival') } catch {}
})
</script>
