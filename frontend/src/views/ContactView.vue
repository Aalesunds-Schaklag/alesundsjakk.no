<template>
  <v-container class="py-12">
    <h1 class="text-h4 font-weight-bold mb-2">{{ t('contact.title') }}</h1>

    <v-row class="mt-6">
      <v-col cols="12" md="6">
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
            <v-btn variant="tonal" color="error" class="mr-2 mb-2">
              <v-icon start>mdi-youtube</v-icon>
              YouTube
            </v-btn>
            <v-alert type="info" variant="tonal" density="compact" class="mt-4">
              {{ t('contact.spond_info') }}
            </v-alert>
          </v-card-text>
        </v-card>
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
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const sending = ref(false)
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
</script>
