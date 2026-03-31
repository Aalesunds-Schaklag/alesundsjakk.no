<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-item>
            <v-card-title>{{ t('nav.login') }}</v-card-title>
          </v-card-item>
          <v-card-text>
            <div v-if="verifying">
              <v-progress-linear indeterminate color="primary" class="mb-4" />
              <p class="text-body-2">Verifiserer innlogging...</p>
            </div>
            <div v-else-if="sent">
              <v-alert v-if="magicLink" type="warning" variant="tonal">
                E-post er ikke konfigurert ennå. Bruk lenken under for å logge inn:
                <br /><br />
                <a :href="magicLink">{{ magicLink }}</a>
              </v-alert>
              <v-alert v-else type="success" variant="tonal">
                Sjekk e-posten din for innloggingslenke!
              </v-alert>
            </div>
            <v-form v-else @submit.prevent="requestLink">
              <p class="text-body-2 mb-4">
                Skriv inn e-postadressen din for å motta en innloggingslenke.
              </p>
              <v-text-field
                v-model="email"
                label="E-post"
                type="email"
                required
                autofocus
              />
              <v-btn type="submit" color="primary" block :loading="loading">
                Send innloggingslenke
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const api = useApi()
const authStore = useAuthStore()

const email = ref('')
const loading = ref(false)
const sent = ref(false)
const magicLink = ref<string | null>(null)
const verifying = ref(false)

onMounted(async () => {
  const token = route.query.token as string
  if (token) {
    verifying.value = true
    try {
      const data = await api.get<any>(`/auth/verify?token=${token}`)
      authStore.setToken(data.access_token)
      router.push('/admin')
    } catch {
      verifying.value = false
    }
  }
})

async function requestLink() {
  loading.value = true
  try {
    const data = await api.post<any>('/auth/request-link', { email: email.value })
    if (data.email_not_configured && data.magic_link) {
      magicLink.value = data.magic_link
    }
    sent.value = true
  } catch {}
  loading.value = false
}
</script>
