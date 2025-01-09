<template>
  <ul class="space-y-4">
    <li v-for="post in posts" :key="post._id">
      <NuxtLink 
        :to="post._path" 
        class="block p-6 rounded-lg border bg-card hover:bg-muted/50 transition"
      >
        <h3 class="text-xl font-semibold group-hover:text-primary">{{ post.title }}</h3>
        <div class="flex items-center space-x-4 mt-2 mb-3 text-sm text-muted-foreground">
          <time class="flex items-center">
            <CalendarIcon class="w-4 h-4 mr-2" />
            {{ formatDate(post.date) }}
          </time>
          <div class="flex items-center space-x-2">
            <NuxtLink
              v-for="tag in post.tags"
              :key="tag"
              :to="`/posts?tag=${tag}`"
              class="hover:text-primary"
              @click.stop
            >
              #{{ tag }}
            </NuxtLink>
          </div>
        </div>
        <p class="text-muted-foreground">{{ post.description }}</p>
      </NuxtLink>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { Calendar as CalendarIcon } from 'lucide-vue-next'

interface Post {
  _id: string
  _path: string
  title: string
  description: string
  date: string
  tags: string[]
}

defineProps<{
  posts: Post[]
}>()

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>