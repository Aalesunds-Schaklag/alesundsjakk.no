<template>
  <v-sheet color="primary" class="py-16 text-center text-white">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <img src="/logo.jpg" alt="Aalesunds Schaklag" height="120" class="mb-6 rounded-lg elevation-4" />
          <h1 class="text-h3 text-md-h2 font-weight-bold mb-2">
            {{ t('home.hero_title') }}
          </h1>
          <p class="text-h6 font-weight-light mb-6" style="color: rgba(255,255,255,0.85)">
            {{ t('home.hero_subtitle') }}
          </p>
          <v-btn
            color="secondary"
            size="large"
            rounded="pill"
            to="/bli-med"
            class="text-primary font-weight-bold"
          >
            <v-icon start>mdi-chess-knight</v-icon>
            {{ t('home.hero_cta') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-sheet>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>
