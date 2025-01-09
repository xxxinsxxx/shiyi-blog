<template>
  <main class="container  mx-16 p-4 md:p-6 lg:p-8">
    <!-- 返回按钮 -->
    <NuxtLink to="/" class="inline-flex items-center mb-6 text-muted-foreground hover:text-foreground">
      <ArrowLeft class="w-4 h-4 mr-2" />
      Back to Home
    </NuxtLink>

    <h1 class="text-3xl font-bold mb-8">Articles</h1>

    <!-- 搜索和标签筛选 -->
    <PostsFilter
      :tags="allTags"
      :selected-tag="selectedTag"
      @update:search="searchQuery = $event"
      @update:selectedTag="selectedTag = $event"
    />

    <!-- 文章列表 -->
    <div class="space-y-6">
      <article
        v-for="post in filteredPosts"
        :key="post._path"
        class="group"

      >
        <NuxtLink :to="post._path"
                  class="block p-6 rounded-lg border bg-card hover:bg-muted/50 transition"
        >
          <h2 class="text-2xl font-semibold group-hover:text-primary transition-colors">
            {{ post.title }}
          </h2>
          <div class="flex items-center space-x-4 mt-2 mb-3 text-sm text-muted-foreground">
            <time class="flex items-center">
              <CalendarIcon class="w-4 h-4 mr-2" />
              {{ formatDate(post.date) }}
            </time>
            <div class="flex items-center space-x-2">
              <span v-for="tag in post.tags" :key="tag"
                class="hover:text-primary cursor-pointer"
                @click.prevent="selectTag(tag)"
              >
                #{{ tag }}
              </span>
            </div>
          </div>
          <p class="text-muted-foreground">{{ post.description }}</p>
        </NuxtLink>
      </article>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ArrowLeft, Calendar as CalendarIcon } from 'lucide-vue-next'

// 获取所有文章
const { data: posts } = await useAsyncData('posts', () =>
  queryContent('posts').sort({ date: -1 }).find()
)

// 搜索和标签状态
const searchQuery = ref('')
const selectedTag = ref<string | null>(null)

// 从路由获取标签参数
const route = useRoute()
onMounted(() => {
  if (route.query.tag) {
    selectedTag.value = route.query.tag as string
  }
})

// 获取所有唯一标签
const allTags = computed(() => {
  const tags = new Set<string>()
  posts.value?.forEach(post => {
    post.tags?.forEach(tag => tags.add(tag))
  })
  return Array.from(tags)
})

// 过滤文章
const filteredPosts = computed(() => {
  if (!posts.value) return []

  return posts.value.filter(post => {
    // 标签筛选
    if (selectedTag.value && !post.tags?.includes(selectedTag.value)) {
      return false
    }

    // 搜索筛选
    if (searchQuery.value) {
      const search = searchQuery.value.toLowerCase()
      return (
        post.title?.toLowerCase().includes(search) ||
        post.description?.toLowerCase().includes(search) ||
        post.tags?.some(tag => tag.toLowerCase().includes(search))
      )
    }

    return true
  })
})

// 格式化日期
function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 选择标签
function selectTag(tag: string) {
  selectedTag.value = tag
}
</script>
