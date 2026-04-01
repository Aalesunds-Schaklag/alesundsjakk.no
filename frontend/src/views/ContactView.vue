<template>
  <v-container class="py-12">
    <h1 class="text-h4 font-weight-bold mb-2">{{ t('contact.title') }}</h1>

    <v-row class="mt-6">
      <v-col cols="12" md="6">
        <!-- Wagtail content -->
        <div v-if="page" v-html="lang === 'en' && page.content_en ? page.content_en : page.content_no" class="text-body-1 wagtail-content" />

        <!-- Fallback if Wagtail unavailable -->
        <template v-else-if="loaded">
          <v-card class="mb-6">
            <v-card-item>
              <v-card-title>{{ t('contact.address') }}</v-card-title>
            </v-card-item>
            <v-card-text>
              <v-list density="compact">
                <v-list-item prepend-icon="mdi-map-marker">
                  <v-list-item-title>Steinvågvegen 60</v-list-item-title>
                  <v-list-item-subtitle>6005 Ålesund (Aspøya)</v-list-item-subtitle>
                </v-list-item>
                <v-list-item prepend-icon="mdi-email">
                  <v-list-item-title>post@alesundsjakk.no</v-list-item-title>
                </v-list-item>
                <v-list-item prepend-icon="mdi-phone">
                  <v-list-item-title>+47 932 58 938</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>

          <v-card class="mb-6">
            <v-card-item>
              <v-card-title>{{ t('contact.social') }}</v-card-title>
            </v-card-item>
            <v-card-text>
              <v-btn
                href="https://www.facebook.com/aalesundsschaklag"
                target="_blank"
                variant="tonal"
                color="primary"
                class="mr-2 mb-2"
              >
                <v-icon start>mdi-facebook</v-icon>
                Facebook
              </v-btn>
              <v-alert type="info" variant="tonal" density="compact" class="mt-4">
                {{ t('contact.spond_info') }}
              </v-alert>
            </v-card-text>
          </v-card>
        </template>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-item>
            <v-card-title>{{ t('contact.form_send') }}</v-card-title>
          </v-card-item>
          <v-card-text>
            <v-form @submit.prevent="send">
              <v-text-field v-model="form.name" :label="t('contact.form_name')" required />
              <v-text-field v-model="form.email" :label="t('contact.form_email')" type="email" required />
              <v-text-field v-model="form.phone" :label="t('contact.form_phone')" />
              <v-textarea v-model="form.message" :label="t('contact.form_message')" rows="5" required />
              <v-btn type="submit" color="primary" block :loading="sending">
                {{ t('contact.form_send') }}
              </v-btn>
            </v-form>
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

const sending = ref(false)
const page = ref<any>(null)
const loaded = ref(false)
const form = reactive({ name: '', email: '', phone: '', message: '' })

async function send() {
  sending.value = true
  try {
    await new Promise(r => setTimeout(r, 500))
    alert('Melding sendt!')
    form.name = ''; form.email = ''; form.phone = ''; form.message = ''
  } finally {
    sending.value = false
  }
}

onMounted(async () => {
  page.value = await getPage('kontakt')
  loaded.value = true
})
</script>

<style scoped>
.wagtail-content :deep(h2) {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}
.wagtail-content :deep(h3) {
  margin-top: 1.25rem;
  margin-bottom: 0.5rem;
}
.wagtail-content :deep(p) {
  margin-bottom: 0.75rem;
}
</style>
