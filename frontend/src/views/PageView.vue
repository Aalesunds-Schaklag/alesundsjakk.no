<template>
  <v-container class="py-12">
    <v-progress-linear v-if="loading" indeterminate color="primary" />
    <div v-if="page">
      <h1 class="text-h4 font-weight-bold mb-6">
        {{ lang === 'en' && page.title_en ? page.title_en : page.title_no }}
      </h1>
      <div v-html="lang === 'en' && page.content_en ? page.content_en : page.content_no" class="text-body-1" />
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useWagtail } from '@/composables/useWagtail'

const { locale } = useI18n()
const lang = locale
const route = useRoute()
const { getPage } = useWagtail()
const page = ref<any>(null)
const loading = ref(true)

async function load() {
  loading.value = true
  page.value = await getPage(route.params.slug as string)
  loading.value = false
}

onMounted(load)
watch(() => route.params.slug, load)
</script>
