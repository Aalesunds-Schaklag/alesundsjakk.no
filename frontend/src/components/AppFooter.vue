<template>
  <v-footer color="primary" class="mt-12 pa-8">
    <v-container>
      <v-row>
        <v-col cols="12" md="4">
          <h4 class="text-subtitle-1 font-weight-bold text-white mb-2">Aalesunds Schaklag</h4>
          <p class="text-body-2" style="color: rgba(255,255,255,0.7)">
            {{ t('common.founded') }} 1913
          </p>
          <p class="text-body-2" style="color: rgba(255,255,255,0.7)">
            Steinvågvegen 60<br>
            6005 Ålesund
          </p>
        </v-col>
        <v-col cols="12" md="4">
          <h4 class="text-subtitle-1 font-weight-bold text-white mb-2">{{ t('contact.social') }}</h4>
          <div class="d-flex ga-2">
            <v-btn icon="mdi-facebook" variant="text" size="small" href="https://www.facebook.com/aalesundsschaklag" target="_blank" />
            <v-btn icon="mdi-youtube" variant="text" size="small" href="#" target="_blank" />
          </div>
          <p class="text-body-2 mt-2" style="color: rgba(255,255,255,0.7)">
            {{ t('contact.spond_info') }}
          </p>
        </v-col>
        <v-col cols="12" md="4">
          <h4 class="text-subtitle-1 font-weight-bold text-white mb-2">Lenker</h4>
          <div class="d-flex flex-column ga-1">
            <a href="https://www.sjakk.no" target="_blank" class="text-body-2" style="color: rgba(255,255,255,0.7)">Norges Sjakkforbund</a>
            <a href="https://lichess.org" target="_blank" class="text-body-2" style="color: rgba(255,255,255,0.7)">Lichess</a>
          </div>
        </v-col>
      </v-row>
      <v-divider class="my-4" style="opacity: 0.2" />
      <p class="text-center text-caption" style="color: rgba(255,255,255,0.5)">
        &copy; {{ new Date().getFullYear() }} Aalesunds Schaklag
      </p>
    </v-container>
  </v-footer>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>
