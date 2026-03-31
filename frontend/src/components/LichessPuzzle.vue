<template>
  <v-card>
    <v-card-item>
      <template v-slot:prepend>
        <v-icon color="secondary" size="large">mdi-puzzle</v-icon>
      </template>
      <v-card-title>{{ t('home.daily_puzzle') }}</v-card-title>
      <v-card-subtitle v-if="puzzle.rating">Rating: {{ puzzle.rating }}</v-card-subtitle>
    </v-card-item>
    <v-card-text v-if="puzzle.gameUrl" class="text-center">
      <iframe
        :src="`https://lichess.org/training/frame?theme=brown&bg=light`"
        style="width: 100%; aspect-ratio: 1; border: none; border-radius: 8px;"
        allowtransparency="true"
      />
    </v-card-text>
    <v-card-actions>
      <v-btn
        v-if="puzzle.gameUrl"
        :href="puzzle.gameUrl"
        target="_blank"
        color="primary"
        variant="text"
      >
        {{ t('home.solve_on_lichess') }}
        <v-icon end>mdi-open-in-new</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const api = useApi()
const puzzle = ref<any>({})

onMounted(async () => {
  try {
    puzzle.value = await api.get('/puzzle')
  } catch {
    // API not available
  }
})
</script>
