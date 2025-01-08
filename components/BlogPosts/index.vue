<template>
    <ul class="space-y-4">
      <li v-for="post in posts" :key="post._id">
        <NuxtLink :to="post._path" class="block hover:bg-muted p-4 rounded-lg transition">
          <h3 class="font-semibold">{{ post.title }}</h3>
          <p class="text-sm text-muted-foreground">{{ post.description }}</p>
          <time class="text-xs text-muted-foreground">{{ formatDate(post.date) }}</time>
        </NuxtLink>
      </li>
    </ul>
  </template>
  
  <script setup lang="ts">
  interface Post {
    _id: string
    _path: string
    title: string
    description: string
    date: string
  }
  
  defineProps<{
    posts: Post[]
  }>()
  
  function formatDate(date: string) {
    return new Date(date).toLocaleDateString()
  }
  </script>