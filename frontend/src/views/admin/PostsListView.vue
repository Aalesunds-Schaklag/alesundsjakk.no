<template>
  <div>
    <div class="d-flex align-center justify-space-between mb-6">
      <h1 class="text-h5 font-weight-bold">{{ t('admin.posts') }}</h1>
      <v-btn color="primary" to="/admin/posts/new">
        <v-icon start>mdi-plus</v-icon>
        {{ t('admin.new_post') }}
      </v-btn>
    </div>

    <v-table>
      <thead>
        <tr>
          <th>{{ t('admin.title') }}</th>
          <th>Type</th>
          <th>{{ t('admin.category') }}</th>
          <th>Status</th>
          <th>Dato</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="post in posts" :key="post.id">
          <td>{{ post.title_no }}</td>
          <td><v-chip size="x-small">{{ post.post_type }}</v-chip></td>
          <td>{{ post.category || '-' }}</td>
          <td>
            <v-chip :color="post.published ? 'success' : 'warning'" size="x-small">
              {{ post.published ? t('admin.publish') : t('admin.draft') }}
            </v-chip>
          </td>
          <td class="text-caption">{{ post.created_at?.slice(0, 10) }}</td>
          <td>
            <v-btn icon="mdi-pencil" size="small" variant="text" :to="`/admin/posts/${post.id}`" />
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="deletePost(post.id)" />
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from '@/composables/useApi'

const { t } = useI18n()
const api = useApi()
const posts = ref<any[]>([])

onMounted(load)

async function load() {
  try { posts.value = await api.get('/admin/posts') } catch {}
}

async function deletePost(id: string) {
  if (confirm('Er du sikker?')) {
    await api.del(`/admin/posts/${id}`)
    await load()
  }
}
</script>
