<template>
  <div>
    <HeroSection />

    <v-container class="py-12">
      <v-row>
        <v-col cols="12" md="8">
          <NextEvents class="mb-12" />
          <NewsTimeline />
        </v-col>

        <v-col cols="12" md="4">
          <LichessPuzzle class="mb-6" />

          <v-card class="mb-6">
            <v-card-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-clock</v-icon>
              </template>
              <v-card-title class="text-body-1">Klubbkveld</v-card-title>
              <v-card-subtitle>Torsdager 19:30 – 21:30</v-card-subtitle>
            </v-card-item>
            <v-card-text class="text-body-2">
              Steinvågvegen 60, 6005 Ålesund
            </v-card-text>
            <v-card-actions>
              <v-btn variant="text" color="primary" to="/bli-med" size="small">
                {{ t('home.hero_cta') }}
              </v-btn>
            </v-card-actions>
          </v-card>

          <v-card>
            <v-card-item>
              <template v-slot:prepend>
                <v-icon color="secondary">mdi-party-popper</v-icon>
              </template>
              <v-card-title class="text-body-1">{{ t('festival.title') }}</v-card-title>
              <v-card-subtitle>Kongsberg Maritime Chess Festival</v-card-subtitle>
            </v-card-item>
            <v-card-actions>
              <v-btn variant="text" color="primary" to="/festival" size="small">
                {{ t('common.read_more') }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <SponsorBar />
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import HeroSection from '@/components/HeroSection.vue'
import NextEvents from '@/components/NextEvents.vue'
import NewsTimeline from '@/components/NewsTimeline.vue'
import LichessPuzzle from '@/components/LichessPuzzle.vue'
import SponsorBar from '@/components/SponsorBar.vue'

const { t } = useI18n()
</script>
