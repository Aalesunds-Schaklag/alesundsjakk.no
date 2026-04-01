<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <h1 class="text-h4 font-weight-bold mb-2">{{ t('join.title') }}</h1>
        <p class="text-subtitle-1 text-medium-emphasis mb-8">{{ t('join.subtitle') }}</p>

        <v-card class="mb-6" color="secondary" variant="tonal">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon color="secondary" size="large">mdi-hand-wave</v-icon>
            </template>
            <v-card-title>{{ t('join.can_i_show_up') }}</v-card-title>
          </v-card-item>
          <v-card-text class="text-body-1">
            {{ t('join.yes_you_can') }}
          </v-card-text>
        </v-card>

        <v-card class="mb-6">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon color="primary">mdi-chess-knight</v-icon>
            </template>
            <v-card-title>{{ t('join.what_happens') }}</v-card-title>
          </v-card-item>
          <v-card-text class="text-body-1">
            {{ t('join.club_evening_desc') }}
          </v-card-text>
        </v-card>

        <v-card class="mb-6">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon color="success">mdi-account-group</v-icon>
            </template>
            <v-card-title>{{ t('join.youth_title') }}</v-card-title>
          </v-card-item>
          <v-card-text>
            <p class="text-body-1 mb-4">{{ t('join.youth_desc') }}</p>
            <v-list density="compact">
              <v-list-item prepend-icon="mdi-map-marker">
                <v-list-item-title>Valderøy barneskule</v-list-item-title>
                <v-list-item-subtitle>Mandager 18:00 – 19:30 | Kontakt: Sergei, 480 71 631</v-list-item-subtitle>
              </v-list-item>
              <v-list-item prepend-icon="mdi-map-marker">
                <v-list-item-title>Spjelkavik barneskole</v-list-item-title>
                <v-list-item-subtitle>Onsdager 17:00 – 19:00 | Kontakt: Mads, 469 86 400</v-list-item-subtitle>
              </v-list-item>
              <v-list-item prepend-icon="mdi-map-marker">
                <v-list-item-title>Aalesunds Schaklag, Steinvågvegen 60</v-list-item-title>
                <v-list-item-subtitle>Torsdager 18:00 – 19:00</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Membership fees from Wagtail -->
        <v-card class="mb-6">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon color="primary">mdi-card-account-details</v-icon>
            </template>
            <v-card-title>{{ t('join.membership') }}</v-card-title>
          </v-card-item>
          <v-card-text>
            <p class="text-body-1 mb-4">{{ t('join.membership_desc') }}</p>
            <v-table v-if="priceItems.length" density="compact">
              <tbody>
                <tr v-for="(item, i) in priceItems" :key="i">
                  <td class="font-weight-medium">
                    {{ lang === 'en' && item.category_en ? item.category_en : item.category_no }}
                  </td>
                  <td class="text-right font-weight-bold" style="white-space: nowrap;">
                    {{ item.price_nok }} kr
                  </td>
                  <td class="text-medium-emphasis">
                    {{ lang === 'en' && item.description_en ? item.description_en : item.description_no }}
                  </td>
                </tr>
              </tbody>
            </v-table>
            <v-btn
              variant="text"
              color="primary"
              to="/om-oss/kontingenter"
              class="mt-2"
            >
              {{ lang === 'en' ? 'Full pricing details' : 'Fullstendig prisoversikt' }}
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-text>
        </v-card>

        <v-card color="primary" variant="tonal">
          <v-card-item>
            <template v-slot:prepend>
              <v-icon color="primary">mdi-phone</v-icon>
            </template>
            <v-card-title>{{ t('join.contact_person') }}</v-card-title>
          </v-card-item>
          <v-card-text>
            <p class="text-body-1">Ta kontakt for spørsmål om klubben:</p>
            <v-btn variant="text" color="primary" to="/kontakt">
              {{ t('nav.contact') }}
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWagtail, type PriceItem } from '@/composables/useWagtail'

const { t, locale } = useI18n()
const lang = locale
const { getPage } = useWagtail()
const priceItems = ref<PriceItem[]>([])

onMounted(async () => {
  const kontingenter = await getPage('kontingenter')
  if (kontingenter?.price_items) {
    priceItems.value = kontingenter.price_items
  }
})
</script>
