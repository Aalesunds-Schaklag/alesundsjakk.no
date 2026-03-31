<template>
  <div>
    <v-btn variant="text" color="primary" to="/admin/posts" class="mb-4">
      <v-icon start>mdi-arrow-left</v-icon>
      {{ t('common.back') }}
    </v-btn>

    <h1 class="text-h5 font-weight-bold mb-6">
      {{ isNew ? t('admin.new_post') : t('admin.edit') }}
    </h1>

    <v-form @submit.prevent="save">
      <v-row>
        <v-col cols="12" md="8">
          <v-text-field v-model="form.title_no" label="Tittel (norsk)" required />
          <v-text-field v-model="form.title_en" label="Title (English)" />
          <v-textarea v-model="form.content_no" label="Innhold (norsk)" rows="12" required />
          <v-textarea v-model="form.content_en" label="Content (English)" rows="8" />
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            v-model="form.post_type"
            :items="[{title: 'Artikkel', value: 'article'}, {title: 'Kort melding', value: 'message'}]"
            label="Type"
          />
          <v-select
            v-model="form.category"
            :items="['turnering', 'klubb', 'ungdom', 'festival', 'annet']"
            label="Kategori"
            clearable
          />
          <v-text-field v-model="form.excerpt_no" label="Utdrag (norsk)" />
          <v-text-field v-model="form.excerpt_en" label="Excerpt (English)" />
          <v-text-field v-model="form.image_url" label="Bilde-URL" />
          <v-switch v-model="form.published" label="Publisert" color="success" />
          <v-btn type="submit" color="primary" block :loading="saving">
            {{ t('admin.save') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const api = useApi()
const saving = ref(false)

const isNew = computed(() => route.params.id === 'new')

const form = reactive({
  title_no: '',
  title_en: '',
  content_no: '',
  content_en: '',
  excerpt_no: '',
  excerpt_en: '',
  post_type: 'article',
  category: null as string | null,
  image_url: '',
  published: false,
})

onMounted(async () => {
  if (!isNew.value) {
    try {
      const posts = await api.get<any[]>('/admin/posts')
      const post = posts.find((p: any) => p.id === route.params.id)
      if (post) Object.assign(form, post)
    } catch {}
  }
})

async function save() {
  saving.value = true
  try {
    if (isNew.value) {
      await api.post('/admin/posts', form)
    } else {
      await api.put(`/admin/posts/${route.params.id}`, form)
    }
    router.push('/admin/posts')
  } catch {}
  saving.value = false
}
</script>
