<template>
  <v-container class="py-12">
    <h1 class="text-h4 font-weight-bold mb-2">{{ t('about.title') }}</h1>

    <div v-if="page" v-html="lang === 'en' && page.content_en ? page.content_en : page.content_no" class="text-body-1 mt-6" />

    <div v-else class="mt-6">
      <v-card class="mb-6">
        <v-card-item>
          <template v-slot:prepend>
            <v-avatar color="primary" size="56">
              <img src="/logo.jpg" alt="Logo" />
            </v-avatar>
          </template>
          <v-card-title>{{ t('about.history') }}</v-card-title>
        </v-card-item>
        <v-card-text class="text-body-1">
          <p>
            Aalesunds Schaklag ble stiftet i 1913 og er en av de eldste sjakklubbene i Norge.
            Klubben holder til i egne lokaler på Steinvågvegen 60 på Aspøya i Ålesund.
          </p>
          <p class="mt-4">
            Klubben arrangerer ukentlige klubbkvelder, turneringer gjennom hele året,
            ungdomssjakk på flere steder i Ålesund-området, og den årlige Ålesund Sjakkfestival.
          </p>
          <p class="mt-4">
            Med over 100 år med sjakk i Ålesund er vi stolte over å tilby et aktivt og
            inkluderende miljø for sjakkspillere i alle aldre og på alle nivåer.
          </p>
        </v-card-text>
      </v-card>

      <v-card class="mb-6">
        <v-card-item>
          <v-card-title>{{ t('about.champions') }}</v-card-title>
        </v-card-item>
        <v-card-text class="text-body-2 text-medium-emphasis">
          Klubbmesterlisten fra 1913 til i dag er tilgjengelig og vil bli publisert her.
        </v-card-text>
      </v-card>

      <v-card>
        <v-card-item>
          <v-card-title>{{ t('about.board') }}</v-card-title>
        </v-card-item>
        <v-card-text class="text-body-2 text-medium-emphasis">
          Informasjon om styret publiseres her.
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWagtail } from '@/composables/useWagtail'

const { t, locale } = useI18n()
const lang = locale
const { getPage } = useWagtail()
const page = ref<any>(null)

onMounted(async () => {
  page.value = await getPage('om-oss')
})
</script>
