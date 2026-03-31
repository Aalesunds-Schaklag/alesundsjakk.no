<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" md="6">
        <h1 class="text-h4 font-weight-bold mb-6">{{ t('home.daily_puzzle') }}</h1>
        <LichessPuzzle />
        <v-card class="mt-6">
          <v-card-text class="text-body-2 text-medium-emphasis">
            Daglig sjakkoppgave fra Lichess. Ny oppgave hver dag!
            <br><br>
            <a href="https://lichess.org/training" target="_blank">
              Flere oppgaver på Lichess
              <v-icon size="small">mdi-open-in-new</v-icon>
            </a>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import LichessPuzzle from '@/components/LichessPuzzle.vue'
const { t } = useI18n()
</script>
