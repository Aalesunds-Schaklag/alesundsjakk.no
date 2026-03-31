import { createI18n } from 'vue-i18n'
import no from '@/locales/no'
import en from '@/locales/en'

export default createI18n({
  legacy: false,
  locale: 'no',
  fallbackLocale: 'no',
  messages: { no, en },
})
