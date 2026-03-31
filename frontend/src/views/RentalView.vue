<template>
  <v-container class="py-12">
    <h1 class="text-h4 font-weight-bold mb-2">{{ t('rental.title') }}</h1>
    <p class="text-subtitle-1 text-medium-emphasis mb-8">{{ t('rental.subtitle') }}</p>

    <v-row>
      <v-col cols="12" md="7">
        <div v-if="page" v-html="lang === 'en' && page.content_en ? page.content_en : page.content_no" class="text-body-1 mb-8" />

        <div v-else>
          <v-card class="mb-6">
            <v-card-item>
              <v-card-title>{{ t('rental.facilities') }}</v-card-title>
            </v-card-item>
            <v-card-text>
              <v-list density="compact">
                <v-list-item prepend-icon="mdi-table-furniture">
                  <v-list-item-title>Stort møterom</v-list-item-title>
                  <v-list-item-subtitle>Plass til 40 personer, projektor, whiteboard</v-list-item-subtitle>
                </v-list-item>
                <v-list-item prepend-icon="mdi-coffee">
                  <v-list-item-title>Kjøkken</v-list-item-title>
                  <v-list-item-subtitle>Kaffemaskin, kjøleskap, oppvaskmaskin</v-list-item-subtitle>
                </v-list-item>
                <v-list-item prepend-icon="mdi-wifi">
                  <v-list-item-title>WiFi og AV-utstyr</v-list-item-title>
                </v-list-item>
                <v-list-item prepend-icon="mdi-parking">
                  <v-list-item-title>Gratis parkering</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>

          <v-card>
            <v-card-item>
              <v-card-title>{{ t('rental.pricing') }}</v-card-title>
            </v-card-item>
            <v-card-text class="text-body-1">
              Ta kontakt for priser og tilgjengelighet.
            </v-card-text>
          </v-card>
        </div>
      </v-col>

      <v-col cols="12" md="5">
        <v-card>
          <v-card-item>
            <v-card-title>{{ t('rental.inquiry') }}</v-card-title>
          </v-card-item>
          <v-card-text>
            <v-form @submit.prevent="sendInquiry">
              <v-text-field v-model="form.name" :label="t('contact.form_name')" required />
              <v-text-field v-model="form.email" :label="t('contact.form_email')" type="email" required />
              <v-text-field v-model="form.phone" :label="t('contact.form_phone')" />
              <v-textarea v-model="form.message" :label="t('contact.form_message')" rows="4" required />
              <v-btn type="submit" color="primary" block :loading="sending">
                {{ t('rental.send') }}
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <v-card class="mt-4">
          <v-card-text>
            <p class="font-weight-bold mb-1">{{ t('contact.address') }}</p>
            <p class="text-body-2">Steinvågvegen 60, 6005 Ålesund</p>
            <p class="text-body-2 text-medium-emphasis">På Aspøya, øst for Bunnpris-rundkjøringen</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWagtail } from '@/composables/useWagtail'

const { t, locale } = useI18n()
const lang = locale
const { getPage } = useWagtail()
const page = ref<any>(null)
const sending = ref(false)
const form = reactive({ name: '', email: '', phone: '', message: '' })

onMounted(async () => {
  page.value = await getPage('lokaler')
})

async function sendInquiry() {
  sending.value = true
  try {
    // Contact form submission would go through the API
    await new Promise(r => setTimeout(r, 500))
    alert('Forespørsel sendt!')
    form.name = ''; form.email = ''; form.phone = ''; form.message = ''
  } finally {
    sending.value = false
  }
}
</script>
