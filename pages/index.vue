<template>
  <main class="container mx-auto p-4 md:p-6 lg:p-8">
    <div class="grid grid-cols-1 md:grid-cols-8 lg:grid-cols-12 gap-4">
      <!-- 左侧栏 -->
      <div class="md:col-span-4 lg:col-span-4 space-y-4">
        <!-- 个人信息 -->
        <Card class="p-4">
          <div class="flex flex-col sm:flex-row items-center sm:items-start space-y-4 sm:space-y-0 sm:space-x-4">
            <Avatar class="w-24 h-24">
              <AvatarImage src="/avatar.jpg" />
              <AvatarFallback>Shiyi</AvatarFallback>
            </Avatar>
            <div class="text-center sm:text-left">
              <h1 class="text-2xl font-bold">Shiyi</h1>
              <p class="text-muted-foreground">Frontend Developer & Designer</p>
            </div>
          </div>
        </Card>

        <!-- 音乐播放器 -->
        <Card>
          <CardHeader>
            <CardTitle>Now Playing</CardTitle>
          </CardHeader>
          <CardContent>
            <MusicWidget />
          </CardContent>
        </Card>

        <!-- 社交媒体和图片 -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Card>
            <CardContent class="p-4">
              <div class="flex flex-col space-y-2">
                <a href="https://github.com/yourusername" target="_blank">
                  <Button variant="ghost" class="w-full justify-start">
                    <Github class="w-5 h-5 mr-2" />
                    Github
                  </Button>
                </a>
                <a href="https://twitter.com/yourusername" target="_blank">
                  <Button variant="ghost" class="w-full justify-start">
                    <Twitter class="w-5 h-5 mr-2" />
                    Twitter
                  </Button>
                </a>
              </div>
            </CardContent>
          </Card>
          <Card class="hidden sm:block">
            <CardContent class="p-4">
              <img src="/assets/images/placeholder.jpg" alt="Placeholder" class="w-full h-32 object-cover rounded-lg" />
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- 中间栏 -->
      <div class="md:col-span-4 lg:col-span-4 flex flex-col gap-4">
        <!-- 功能导航 -->
        <div class="grid grid-cols-3 gap-4">
          <NuxtLink to="/posts" class="block">
            <Card class="hover:bg-muted/50 transition h-full">
              <CardContent class="p-4 text-center">
                <FileText class="w-6 h-6 mx-auto mb-2" />
                <span>Articles</span>
              </CardContent>
            </Card>
          </NuxtLink>
          <NuxtLink to="/movies" class="block">
            <Card class="hover:bg-muted/50 transition h-full">
              <CardContent class="p-4 text-center">
                <Film class="w-6 h-6 mx-auto mb-2" />
                <span>Movies</span>
              </CardContent>
            </Card>
          </NuxtLink>
          <Card class="hover:bg-muted/50 transition h-full">
            <CardContent class="p-4 text-center">
              <Plus class="w-6 h-6 mx-auto mb-2" />
              <span>More</span>
            </CardContent>
          </Card>
        </div>

        <!-- 文字内容 -->
        <Card class="flex-grow">
          <CardContent class="p-6 h-full">
            <p class="text-muted-foreground">
              这里是一段介绍文字，可以描述你自己或者你的网站。这是一个占位符文本，你可以替换成任何你想要展示的内容。
            </p>
          </CardContent>
        </Card>

        <!-- 底部图片 -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Card>
            <CardContent class="p-4">
              <img src="/assets/images/placeholder.jpg" alt="Placeholder" class="w-full h-48 object-cover rounded-lg" />
            </CardContent>
          </Card>
          <Card class="hidden sm:block">
            <CardContent class="p-4">
              <img src="/assets/images/placeholder.jpg" alt="Placeholder" class="w-full h-48 object-cover rounded-lg" />
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- 右侧栏 -->
      <div class="md:col-span-8 lg:col-span-4 lg:row-span-2 space-y-4">
        <!-- 电影滚动封面 -->
        <Card>
          <CardHeader>
            <CardTitle>Featured Movies</CardTitle>
          </CardHeader>
          <CardContent>
            <MovieSlider :movies="movies" />
          </CardContent>
        </Card>

        <!-- 其他内容卡片 -->
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-muted rounded-full"></div>
                <div>
                  <h4 class="font-medium">Activity Title</h4>
                  <p class="text-sm text-muted-foreground">Activity description</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- 占位图片 -->
        <Card class="hidden md:block">
          <CardContent class="p-4">
            <img src="/assets/images/placeholder.jpg" alt="Placeholder" class="w-full h-64 object-cover rounded-lg" />
          </CardContent>
        </Card>
      </div>

      <!-- 最新文章 -->
      <div class="md:col-span-8 lg:col-span-8 space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Latest Posts</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <NuxtLink 
                v-for="post in posts" 
                :key="post._path" 
                :to="post._path"
                class="block p-4 rounded-lg hover:bg-muted/50 transition"
              >
                <h3 class="font-medium">{{ post.title }}</h3>
                <p class="text-sm text-muted-foreground line-clamp-2">{{ post.description }}</p>
                <time class="text-xs text-muted-foreground">{{ formatDate(post.date) }}</time>
              </NuxtLink>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Github, Twitter, FileText, Film, Plus } from 'lucide-vue-next'

// 电影数据
const movies = ref([
  {
    id: 1,
    title: "Inception",
    poster: "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg"
  },
  {
    id: 2,
    title: "The Dark Knight",
    poster: "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
  },
  {
    id: 3,
    title: "Interstellar",
    poster: "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
  },
  // 可以添加更多电影
])
// 获取最新文章
const { data: posts } = await useAsyncData('posts', () => 
  queryContent('posts')
    .sort({ date: -1 }) // 按日期降序
    .limit(3) // 只显示最新的3篇
    .find()
)

// 格式化日期
function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>