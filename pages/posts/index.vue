<template>
  <main class="container mx-auto p-4 md:p-6 lg:p-8">
    <!-- 返回按钮 -->
    <NuxtLink to="/" class="inline-flex items-center mb-6 text-muted-foreground hover:text-foreground">
      <ArrowLeft class="w-4 h-4 mr-2" />
      Back to Home
    </NuxtLink>

    <h1 class="text-3xl font-bold mb-8">Articles</h1>

    <!-- 文章列表 -->
    <div class="grid gap-6">
      <NuxtLink 
        v-for="post in posts" 
        :key="post._path" 
        :to="post._path"
        class="block p-6 rounded-lg border bg-card hover:bg-muted/50 transition"
      >
        <article>
          <h2 class="text-2xl font-semibold mb-2">{{ post.title }}</h2>
          <p class="text-muted-foreground mb-4">{{ post.description }}</p>
          <div class="flex items-center text-sm text-muted-foreground">
            <CalendarIcon class="w-4 h-4 mr-2" />
            <time>{{ formatDate(post.date) }}</time>
          </div>
        </article>
      </NuxtLink>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ArrowLeft, Calendar as CalendarIcon } from 'lucide-vue-next'

// 获取所有文章
const { data: posts } = await useAsyncData('posts-list', () => 
  queryContent('posts')
    .sort({ date: -1 }) // 按日期降序
    .find()
)

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script> 