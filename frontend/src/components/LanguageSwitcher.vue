<template>
  <v-btn-toggle
    :model-value="locale"
    mandatory
    density="compact"
    variant="text"
    class="mx-2"
  >
    <v-btn value="no" size="x-small" @click="switchLang('no')">NO</v-btn>
    <v-btn value="en" size="x-small" @click="switchLang('en')">EN</v-btn>
  </v-btn-toggle>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useAppStore } from '@/stores/app'

const { locale } = useI18n()
const appStore = useAppStore()

function switchLang(lang: string) {
  locale.value = lang
  appStore.setLocale(lang)
}
</script>
