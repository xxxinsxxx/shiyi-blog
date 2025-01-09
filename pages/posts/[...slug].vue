<template>
  <main class="container  mx-16 p-4 md:p-6 lg:p-8">
    <!-- 返回按钮 -->
    <button 
      @click="router.back()" 
      class="inline-flex items-center mb-6 text-muted-foreground hover:text-foreground"
    >
      <ArrowLeft class="w-4 h-4 mr-2" />
      Back
    </button>

    <article class="prose prose-lg dark:prose-invert max-w-none mx-auto">
      <h1>{{ data?.title }}</h1>
      
      <!-- 文章信息 -->
      <div class="flex items-center space-x-4 mt-2 mb-8 text-sm text-muted-foreground not-prose">
        <time>{{ formatDate(data?.date) }}</time>
        <div class="flex items-center space-x-2">
          <NuxtLink
            v-for="tag in data?.tags"
            :key="tag"
            :to="`/posts?tag=${tag}`"
            class="hover:text-primary"
          >
            #{{ tag }}
          </NuxtLink>
        </div>
        <template v-if="data?.description">
            <span>·</span>
            <span>{{ data.description }}</span>
          </template>
      </div>
    
      <ContentRenderer v-if="data" :value="data" />
    </article>
  </main>
</template>

<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'

const router = useRouter()
const { path } = useRoute()

// 获取文章内容
const { data } = await useAsyncData(`content-${path}`, () => {
  return queryContent().where({ _path: path }).findOne()
})

// 如果文章不存在，返回404
if (!data.value) {
  throw createError({
    statusCode: 404,
    message: 'Article not found'
  })
}

// 格式化日期
function formatDate(date: string) {
  try {
    // 确保日期格式正确（YYYY-MM-DD）
    const dateObj = new Date(date)
    if (isNaN(dateObj.getTime())) {
      return 'No date'
    }
    
    return dateObj.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
    console.error('Date parsing error:', e)
    return 'Invalid date'
  }
}
</script>

<style scoped>
.prose {
  max-width: 65ch;
}
</style> 